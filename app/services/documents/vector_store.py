"""
خدمة قاعدة البيانات المتجهة
Vector Store Service using PostgreSQL pgvector
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
import numpy as np

from app.models.documents import Document, DocumentChunk


class VectorStoreService:
    """خدمة البحث في الـ Vector Store"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_chunks(
        self,
        document_id: UUID,
        chunks: List[Dict[str, Any]]
    ) -> int:
        """
        إضافة chunks مع embeddings
        Add document chunks with embeddings
        """

        added = 0
        for chunk in chunks:
            db_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk["index"],
                content=chunk["content"],
                token_count=chunk.get("token_count"),
                page_number=chunk.get("page_number"),
                start_char=chunk.get("start_char"),
                end_char=chunk.get("end_char"),
                embedding=chunk.get("embedding"),
                embedding_model=chunk.get("model"),
                chunk_metadata=chunk.get("metadata")
            )
            self.db.add(db_chunk)
            added += 1

        await self.db.commit()
        return added

    async def search_similar(
        self,
        query_embedding: List[float],
        user_id: UUID,
        limit: int = 10,
        threshold: float = 0.7,
        document_ids: Optional[List[UUID]] = None,
        collection_id: Optional[UUID] = None
    ) -> List[Dict[str, Any]]:
        """
        البحث عن chunks مشابهة
        Search for similar chunks using vector similarity
        """

        # Build query with pgvector
        embedding_str = f"[{','.join(map(str, query_embedding))}]"

        query = f"""
            SELECT
                dc.id,
                dc.document_id,
                dc.content,
                dc.chunk_index,
                dc.page_number,
                d.original_filename,
                1 - (dc.embedding <=> '{embedding_str}'::vector) as similarity
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            WHERE d.user_id = :user_id
            AND dc.embedding IS NOT NULL
        """

        params = {"user_id": str(user_id)}

        if document_ids:
            query += " AND dc.document_id = ANY(:doc_ids)"
            params["doc_ids"] = [str(d) for d in document_ids]

        query += f"""
            AND 1 - (dc.embedding <=> '{embedding_str}'::vector) > :threshold
            ORDER BY dc.embedding <=> '{embedding_str}'::vector
            LIMIT :limit
        """
        params["threshold"] = threshold
        params["limit"] = limit

        result = await self.db.execute(text(query), params)
        rows = result.fetchall()

        results = []
        for row in rows:
            results.append({
                "chunk_id": str(row.id),
                "document_id": str(row.document_id),
                "filename": row.original_filename,
                "content": row.content,
                "chunk_index": row.chunk_index,
                "page_number": row.page_number,
                "similarity": float(row.similarity)
            })

        return results

    async def get_document_chunks(
        self,
        document_id: UUID,
        include_embeddings: bool = False
    ) -> List[DocumentChunk]:
        """الحصول على chunks مستند"""

        query = select(DocumentChunk).where(
            DocumentChunk.document_id == document_id
        ).order_by(DocumentChunk.chunk_index)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_document_chunks(self, document_id: UUID) -> int:
        """حذف chunks مستند"""

        result = await self.db.execute(
            text("DELETE FROM document_chunks WHERE document_id = :doc_id"),
            {"doc_id": str(document_id)}
        )
        await self.db.commit()
        return result.rowcount
