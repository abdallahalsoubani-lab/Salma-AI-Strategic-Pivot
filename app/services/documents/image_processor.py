"""
معالج الصور مع OCR
Image Processor with OCR support
"""

from pathlib import Path
from typing import Dict, Any
from PIL import Image
import pytesseract
import io

from .base_processor import BaseDocumentProcessor, ProcessedDocument


class ImageProcessor(BaseDocumentProcessor):
    """معالج الصور مع OCR"""

    supported_extensions = [".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".gif"]
    processor_name = "image"

    def __init__(self, tesseract_path: str = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    async def process(self, file_path: Path) -> ProcessedDocument:
        """معالجة الصورة واستخراج النص بـ OCR"""

        image = Image.open(str(file_path))

        # Preprocess image for better OCR
        processed_image = self._preprocess_image(image)

        # OCR with Arabic + English support
        text = pytesseract.image_to_string(
            processed_image,
            lang='ara+eng',
            config='--psm 3'  # Fully automatic page segmentation
        )

        # Get detailed OCR data
        ocr_data = pytesseract.image_to_data(
            processed_image,
            lang='ara+eng',
            output_type=pytesseract.Output.DICT
        )

        # Calculate confidence
        confidences = [int(c) for c in ocr_data['conf'] if int(c) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        metadata = await self.extract_metadata(file_path)
        metadata["ocr_confidence"] = avg_confidence

        return ProcessedDocument(
            text=text.strip(),
            pages=[text.strip()],
            page_count=1,
            word_count=self.count_words(text),
            language=self.detect_language(text),
            metadata=metadata,
            tables=[],
            images=[{
                "width": image.width,
                "height": image.height,
                "mode": image.mode,
                "format": image.format
            }]
        )

    async def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """استخراج البيانات الوصفية من الصورة"""

        image = Image.open(str(file_path))

        metadata = {
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "mode": image.mode,
            "size_bytes": file_path.stat().st_size
        }

        # EXIF data if available
        exif = image.getexif()
        if exif:
            metadata["exif"] = {k: str(v) for k, v in exif.items()}

        return metadata

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """تحسين الصورة للـ OCR"""

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert to grayscale
        gray = image.convert('L')

        # Increase contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)

        # Resize if too small
        min_width = 1000
        if enhanced.width < min_width:
            ratio = min_width / enhanced.width
            new_size = (int(enhanced.width * ratio), int(enhanced.height * ratio))
            enhanced = enhanced.resize(new_size, Image.LANCZOS)

        return enhanced
