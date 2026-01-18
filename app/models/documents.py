"""
نماذج معالجة المستندات
Document Processing Models
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, ForeignKey, Enum, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class DocumentType(str, enum.Enum):
    """أنواع المستندات"""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    XLSX = "xlsx"
    XLS = "xls"
    PPTX = "pptx"
    TXT = "txt"
    CSV = "csv"
    IMAGE = "image"  # jpg, png, etc.
    SCANNED = "scanned"  # Scanned documents requiring OCR


class ProcessingStatus(str, enum.Enum):
    """حالة المعالجة"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIALLY_COMPLETED = "partially_completed"


class Document(Base):
    """
    المستند الرئيسي
    Main Document record
    """
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # File info
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)  # UUID-based name
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)

    # Processing
    status = Column(Enum(ProcessingStatus), default=ProcessingStatus.PENDING)
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    processing_error = Column(Text, nullable=True)

    # Extracted content
    extracted_text = Column(Text, nullable=True)
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    language_detected = Column(String(10), nullable=True)  # ar, en, etc.

    # Metadata
    title = Column(String(500), nullable=True)
    author = Column(String(255), nullable=True)
    created_date = Column(DateTime, nullable=True)
    custom_metadata = Column(JSON, nullable=True)

    # Vector embedding info
    is_embedded = Column(Boolean, default=False)
    embedding_model = Column(String(100), nullable=True)
    chunk_count = Column(Integer, nullable=True)

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    user = relationship("User", back_populates="documents")


class DocumentChunk(Base):
    """
    أجزاء المستند للـ Vector Search
    Document chunks for vector search
    """
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)

    # Chunk info
    chunk_index = Column(Integer, nullable=False)  # Order in document
    content = Column(Text, nullable=False)
    token_count = Column(Integer, nullable=True)

    # Source location
    page_number = Column(Integer, nullable=True)
    start_char = Column(Integer, nullable=True)
    end_char = Column(Integer, nullable=True)

    # Embedding
    embedding = Column(ARRAY(Float), nullable=True)  # Vector embedding
    embedding_model = Column(String(100), nullable=True)

    # Metadata
    chunk_metadata = Column(JSON, nullable=True)  # headers, tables, etc.

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="chunks")


class DocumentCollection(Base):
    """
    مجموعة مستندات
    Collection of documents for organized retrieval
    """
    __tablename__ = "document_collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False)
    name_ar = Column(String(255), nullable=True)  # Arabic name
    description = Column(Text, nullable=True)

    # Stats
    document_count = Column(Integer, default=0)
    total_chunks = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DocumentCollectionMapping(Base):
    """ربط المستندات بالمجموعات"""
    __tablename__ = "document_collection_mappings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("document_collections.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
