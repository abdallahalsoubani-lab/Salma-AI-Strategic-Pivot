"""
خدمة المستندات الرئيسية
Main Document Service - Orchestrates all document processing
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from pathlib import Path
from datetime import datetime
import aiofiles
import uuid as uuid_lib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.documents import Document, DocumentType, ProcessingStatus
from app.config import settings

from .pdf_processor import PDFProcessor, ScannedPDFProcessor
from .word_processor import WordProcessor
from .excel_processor import ExcelProcessor
from .image_processor import ImageProcessor
from .chunker import TextChunker, ChunkerConfig
from .embedding_service import EmbeddingService
from .vector_store import VectorStoreService


class DocumentService:
    """خدمة المستندات الرئيسية"""

    UPLOAD_DIR = Path(settings.UPLOAD_DIR)

    # Processor mapping
    PROCESSORS = {
        DocumentType.PDF: PDFProcessor,
        DocumentType.DOCX: WordProcessor,
        DocumentType.DOC: WordProcessor,
        DocumentType.XLSX: ExcelProcessor,
        DocumentType.XLS: ExcelProcessor,
        DocumentType.CSV: ExcelProcessor,
        DocumentType.IMAGE: ImageProcessor,
        DocumentType.SCANNED: ScannedPDFProcessor,
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.chunker = TextChunker(ChunkerConfig(
            chunk_size=1000,
            chunk_overlap=200
        ))
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService(db)

    async def upload_document(
        self,
        user_id: UUID,
        filename: str,
        content: bytes,
        mime_type: str
    ) -> Document:
        """
        رفع مستند جديد
        Upload a new document
        """

        # Determine document type
        doc_type = self._get_document_type(filename, mime_type)

        # Generate unique filename
        file_ext = Path(filename).suffix
        stored_filename = f"{uuid_lib.uuid4()}{file_ext}"
        file_path = self.UPLOAD_DIR / str(user_id) / stored_filename

        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        # Create database record
        document = Document(
            user_id=user_id,
            original_filename=filename,
            stored_filename=stored_filename,
            file_path=str(file_path),
            file_size_bytes=len(content),
            mime_type=mime_type,
            document_type=doc_type,
            status=ProcessingStatus.PENDING
        )

        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)

        return document

    async def process_document(self, document_id: UUID) -> Document:
        """
        معالجة المستند
        Process uploaded document
        """

        # Get document
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise ValueError("Document not found")

        # Update status
        document.status = ProcessingStatus.PROCESSING
        document.processing_started_at = datetime.utcnow()
        await self.db.commit()

        try:
            # Get appropriate processor
            processor_class = self.PROCESSORS.get(document.document_type)
            if not processor_class:
                raise ValueError(f"No processor for type: {document.document_type}")

            processor = processor_class()
            file_path = Path(document.file_path)

            # Process document
            processed = await processor.process(file_path)

            # Update document with extracted data
            document.extracted_text = processed.text
            document.page_count = processed.page_count
            document.word_count = processed.word_count
            document.language_detected = processed.language
            document.title = processed.metadata.get("title")
            document.author = processed.metadata.get("author")
            document.custom_metadata = processed.metadata

            # Chunk the text
            chunks = self.chunker.chunk_text(processed.text)

            # Generate embeddings
            chunk_texts = [c.content for c in chunks]
            embeddings = await self.embedding_service.embed_texts(chunk_texts)

            # Store chunks with embeddings
            chunk_data = []
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                chunk_data.append({
                    "index": chunk.index,
                    "content": chunk.content,
                    "token_count": chunk.token_count,
                    "page_number": chunk.page_number,
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char,
                    "embedding": emb.embedding,
                    "model": emb.model,
                    "metadata": chunk.metadata
                })

            await self.vector_store.add_chunks(document.id, chunk_data)

            # Update document status
            document.is_embedded = True
            document.embedding_model = embeddings[0].model if embeddings else None
            document.chunk_count = len(chunks)
            document.status = ProcessingStatus.COMPLETED
            document.processing_completed_at = datetime.utcnow()

        except Exception as e:
            document.status = ProcessingStatus.FAILED
            document.processing_error = str(e)
            document.processing_completed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(document)

        return document

    async def search_documents(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10,
        document_ids: Optional[List[UUID]] = None
    ) -> List[Dict[str, Any]]:
        """
        البحث في المستندات
        Search documents using semantic similarity
        """

        # Generate query embedding
        query_embedding = await self.embedding_service.embed_text(query)

        # Search vector store
        results = await self.vector_store.search_similar(
            query_embedding=query_embedding.embedding,
            user_id=user_id,
            limit=limit,
            document_ids=document_ids
        )

        return results

    async def get_document(self, document_id: UUID) -> Optional[Document]:
        """الحصول على مستند"""
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()

    async def list_documents(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[Document]:
        """قائمة مستندات المستخدم"""
        result = await self.db.execute(
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.uploaded_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def delete_document(self, document_id: UUID) -> bool:
        """حذف مستند"""
        document = await self.get_document(document_id)
        if not document:
            return False

        # Delete file
        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()

        # Delete from database (cascade will delete chunks)
        await self.db.delete(document)
        await self.db.commit()

        return True

    def _get_document_type(self, filename: str, mime_type: str) -> DocumentType:
        """تحديد نوع المستند"""
        ext = Path(filename).suffix.lower()

        type_map = {
            ".pdf": DocumentType.PDF,
            ".docx": DocumentType.DOCX,
            ".doc": DocumentType.DOC,
            ".xlsx": DocumentType.XLSX,
            ".xls": DocumentType.XLS,
            ".csv": DocumentType.CSV,
            ".pptx": DocumentType.PPTX,
            ".txt": DocumentType.TXT,
            ".jpg": DocumentType.IMAGE,
            ".jpeg": DocumentType.IMAGE,
            ".png": DocumentType.IMAGE,
            ".tiff": DocumentType.IMAGE,
        }

        return type_map.get(ext, DocumentType.TXT)
