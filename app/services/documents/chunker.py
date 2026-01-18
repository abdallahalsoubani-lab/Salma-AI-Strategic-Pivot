"""
خدمة تقسيم النصوص
Text Chunking Service for Vector Embeddings
"""

from typing import List, Optional
import re
from dataclasses import dataclass

from .base_processor import DocumentChunkResult


@dataclass
class ChunkerConfig:
    """إعدادات التقسيم"""
    chunk_size: int = 1000  # Characters per chunk
    chunk_overlap: int = 200  # Overlap between chunks
    min_chunk_size: int = 100  # Minimum chunk size
    split_by: str = "sentence"  # sentence, paragraph, fixed


class TextChunker:
    """خدمة تقسيم النصوص للـ Vector Search"""

    def __init__(self, config: ChunkerConfig = None):
        self.config = config or ChunkerConfig()

    def chunk_text(
        self,
        text: str,
        page_numbers: Optional[List[int]] = None
    ) -> List[DocumentChunkResult]:
        """
        تقسيم النص إلى أجزاء
        Split text into chunks for embedding
        """

        if self.config.split_by == "sentence":
            return self._chunk_by_sentence(text)
        elif self.config.split_by == "paragraph":
            return self._chunk_by_paragraph(text)
        else:
            return self._chunk_fixed(text)

    def _chunk_by_sentence(self, text: str) -> List[DocumentChunkResult]:
        """تقسيم حسب الجمل"""

        # Split into sentences (Arabic + English)
        sentence_pattern = r'(?<=[.!?؟،])\s+'
        sentences = re.split(sentence_pattern, text)

        chunks = []
        current_chunk = ""
        current_start = 0
        chunk_index = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding this sentence exceeds chunk size
            if len(current_chunk) + len(sentence) > self.config.chunk_size:
                # Save current chunk
                if len(current_chunk) >= self.config.min_chunk_size:
                    chunks.append(DocumentChunkResult(
                        content=current_chunk.strip(),
                        index=chunk_index,
                        page_number=None,
                        start_char=current_start,
                        end_char=current_start + len(current_chunk),
                        token_count=len(current_chunk) // 4,  # Rough estimate
                        metadata={}
                    ))
                    chunk_index += 1

                # Start new chunk with overlap
                overlap_text = self._get_overlap(current_chunk)
                current_start = current_start + len(current_chunk) - len(overlap_text)
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence

        # Don't forget last chunk
        if len(current_chunk) >= self.config.min_chunk_size:
            chunks.append(DocumentChunkResult(
                content=current_chunk.strip(),
                index=chunk_index,
                page_number=None,
                start_char=current_start,
                end_char=current_start + len(current_chunk),
                token_count=len(current_chunk) // 4,
                metadata={}
            ))

        return chunks

    def _chunk_by_paragraph(self, text: str) -> List[DocumentChunkResult]:
        """تقسيم حسب الفقرات"""

        paragraphs = text.split('\n\n')
        chunks = []
        chunk_index = 0
        current_pos = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If paragraph is too long, split it
            if len(para) > self.config.chunk_size:
                sub_chunks = self._chunk_by_sentence(para)
                for sub in sub_chunks:
                    sub.index = chunk_index
                    sub.start_char += current_pos
                    sub.end_char += current_pos
                    chunks.append(sub)
                    chunk_index += 1
            else:
                chunks.append(DocumentChunkResult(
                    content=para,
                    index=chunk_index,
                    page_number=None,
                    start_char=current_pos,
                    end_char=current_pos + len(para),
                    token_count=len(para) // 4,
                    metadata={}
                ))
                chunk_index += 1

            current_pos += len(para) + 2  # +2 for \n\n

        return chunks

    def _chunk_fixed(self, text: str) -> List[DocumentChunkResult]:
        """تقسيم بحجم ثابت"""

        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(start + self.config.chunk_size, len(text))

            # Try to break at word boundary
            if end < len(text):
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space

            chunk_text = text[start:end].strip()

            if len(chunk_text) >= self.config.min_chunk_size:
                chunks.append(DocumentChunkResult(
                    content=chunk_text,
                    index=chunk_index,
                    page_number=None,
                    start_char=start,
                    end_char=end,
                    token_count=len(chunk_text) // 4,
                    metadata={}
                ))
                chunk_index += 1

            start = end - self.config.chunk_overlap

        return chunks

    def _get_overlap(self, text: str) -> str:
        """الحصول على نص التداخل"""
        if len(text) <= self.config.chunk_overlap:
            return text

        overlap = text[-self.config.chunk_overlap:]
        # Try to start at word boundary
        first_space = overlap.find(' ')
        if first_space > 0:
            overlap = overlap[first_space + 1:]

        return overlap
