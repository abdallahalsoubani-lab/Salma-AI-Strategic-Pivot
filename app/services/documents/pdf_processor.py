"""
معالج PDF
PDF Document Processor
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, Any, List
import io

from .base_processor import BaseDocumentProcessor, ProcessedDocument


class PDFProcessor(BaseDocumentProcessor):
    """معالج مستندات PDF"""

    supported_extensions = [".pdf"]
    processor_name = "pdf"

    async def process(self, file_path: Path) -> ProcessedDocument:
        """معالجة PDF واستخراج النص"""

        doc = fitz.open(str(file_path))

        pages = []
        tables = []
        images = []
        full_text = []

        for page_num, page in enumerate(doc):
            # Extract text
            page_text = page.get_text("text")
            pages.append(page_text)
            full_text.append(page_text)

            # Extract tables (basic detection)
            tables_on_page = self._extract_tables(page)
            for table in tables_on_page:
                table["page"] = page_num + 1
                tables.append(table)

            # Extract images info
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                images.append({
                    "page": page_num + 1,
                    "index": img_index,
                    "width": img[2],
                    "height": img[3]
                })

        combined_text = "\n\n".join(full_text)

        # Get metadata
        metadata = await self.extract_metadata(file_path)

        doc.close()

        return ProcessedDocument(
            text=combined_text,
            pages=pages,
            page_count=len(pages),
            word_count=self.count_words(combined_text),
            language=self.detect_language(combined_text),
            metadata=metadata,
            tables=tables,
            images=images
        )

    async def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """استخراج البيانات الوصفية من PDF"""

        doc = fitz.open(str(file_path))
        metadata = doc.metadata

        result = {
            "title": metadata.get("title"),
            "author": metadata.get("author"),
            "subject": metadata.get("subject"),
            "keywords": metadata.get("keywords"),
            "creator": metadata.get("creator"),
            "producer": metadata.get("producer"),
            "created_date": metadata.get("creationDate"),
            "modified_date": metadata.get("modDate"),
            "page_count": len(doc),
            "encrypted": doc.is_encrypted
        }

        doc.close()
        return result

    def _extract_tables(self, page) -> List[Dict[str, Any]]:
        """استخراج الجداول من الصفحة (بسيط)"""
        # Basic table detection using text blocks
        # For production, use tabula-py or camelot
        tables = []

        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block.get("type") == 0:  # Text block
                lines = block.get("lines", [])
                # Simple heuristic: multiple aligned columns
                if len(lines) > 2:
                    # Check if it looks like a table
                    pass

        return tables


class ScannedPDFProcessor(PDFProcessor):
    """معالج PDF الممسوح (يحتاج OCR)"""

    processor_name = "scanned_pdf"

    async def process(self, file_path: Path) -> ProcessedDocument:
        """معالجة PDF ممسوح مع OCR"""

        doc = fitz.open(str(file_path))

        pages = []
        full_text = []

        for page_num, page in enumerate(doc):
            # First try normal text extraction
            page_text = page.get_text("text").strip()

            # If no text, use OCR
            if len(page_text) < 50:  # Likely scanned
                page_text = await self._ocr_page(page)

            pages.append(page_text)
            full_text.append(page_text)

        combined_text = "\n\n".join(full_text)
        metadata = await self.extract_metadata(file_path)

        doc.close()

        return ProcessedDocument(
            text=combined_text,
            pages=pages,
            page_count=len(pages),
            word_count=self.count_words(combined_text),
            language=self.detect_language(combined_text),
            metadata=metadata,
            tables=[],
            images=[]
        )

    async def _ocr_page(self, page) -> str:
        """OCR لصفحة واحدة"""
        # Convert page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
        img_bytes = pix.tobytes("png")

        # Use Tesseract OCR
        try:
            from PIL import Image
            import pytesseract

            image = Image.open(io.BytesIO(img_bytes))

            # OCR with Arabic + English support
            text = pytesseract.image_to_string(
                image,
                lang='ara+eng',
                config='--psm 1'  # Automatic page segmentation with OSD
            )

            return text
        except Exception as e:
            return f"[OCR Error: {str(e)}]"
