"""
معالج المستندات الأساسي
Base Document Processor
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProcessedDocument:
    """نتيجة معالجة المستند"""
    text: str
    pages: List[str]  # Text per page
    page_count: int
    word_count: int
    language: str
    metadata: Dict[str, Any]
    tables: List[Dict[str, Any]]  # Extracted tables
    images: List[Dict[str, Any]]  # Image descriptions/OCR


@dataclass
class DocumentChunkResult:
    """نتيجة تقسيم المستند"""
    content: str
    index: int
    page_number: Optional[int]
    start_char: int
    end_char: int
    token_count: int
    metadata: Dict[str, Any]


class BaseDocumentProcessor(ABC):
    """Base class for document processors"""

    supported_extensions: List[str] = []
    processor_name: str = "base"

    @abstractmethod
    async def process(self, file_path: Path) -> ProcessedDocument:
        """
        معالجة المستند واستخراج النص
        Process document and extract text
        """
        pass

    @abstractmethod
    async def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        استخراج البيانات الوصفية
        Extract document metadata
        """
        pass

    def detect_language(self, text: str) -> str:
        """
        اكتشاف لغة النص
        Detect text language
        """
        # Simple Arabic detection
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06FF')
        total_chars = len(text.replace(" ", ""))

        if total_chars == 0:
            return "en"

        arabic_ratio = arabic_chars / total_chars
        return "ar" if arabic_ratio > 0.3 else "en"

    def count_words(self, text: str) -> int:
        """عد الكلمات"""
        return len(text.split())
