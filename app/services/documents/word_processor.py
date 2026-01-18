"""
معالج Word
Word Document Processor (DOCX/DOC)
"""

from pathlib import Path
from typing import Dict, Any, List
from docx import Document as DocxDocument
from docx.table import Table

from .base_processor import BaseDocumentProcessor, ProcessedDocument


class WordProcessor(BaseDocumentProcessor):
    """معالج مستندات Word"""

    supported_extensions = [".docx", ".doc"]
    processor_name = "word"

    async def process(self, file_path: Path) -> ProcessedDocument:
        """معالجة Word واستخراج النص"""

        doc = DocxDocument(str(file_path))

        paragraphs = []
        tables = []

        # Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        # Extract tables
        for table_idx, table in enumerate(doc.tables):
            table_data = self._extract_table(table)
            tables.append({
                "index": table_idx,
                "rows": len(table.rows),
                "columns": len(table.columns),
                "data": table_data
            })

        combined_text = "\n\n".join(paragraphs)

        # Add table text to combined text
        for table in tables:
            for row in table["data"]:
                combined_text += "\n" + " | ".join(row)

        metadata = await self.extract_metadata(file_path)

        return ProcessedDocument(
            text=combined_text,
            pages=[combined_text],  # Word doesn't have clear page breaks
            page_count=1,
            word_count=self.count_words(combined_text),
            language=self.detect_language(combined_text),
            metadata=metadata,
            tables=tables,
            images=[]
        )

    async def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """استخراج البيانات الوصفية"""

        doc = DocxDocument(str(file_path))
        props = doc.core_properties

        return {
            "title": props.title,
            "author": props.author,
            "subject": props.subject,
            "keywords": props.keywords,
            "created": props.created.isoformat() if props.created else None,
            "modified": props.modified.isoformat() if props.modified else None,
            "last_modified_by": props.last_modified_by,
            "revision": props.revision,
            "category": props.category
        }

    def _extract_table(self, table: Table) -> List[List[str]]:
        """استخراج بيانات الجدول"""
        data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            data.append(row_data)
        return data
