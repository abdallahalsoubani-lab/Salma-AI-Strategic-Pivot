"""SQLAlchemy database models for Salma AI Gateway"""
from datetime import datetime
from uuid import uuid4
from enum import Enum as PyEnum
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    Enum,
    ForeignKey,
    Text,
    Numeric,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(str, PyEnum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"


class ConnectionType(str, PyEnum):
    """Data source connection type"""
    ORACLE = "oracle"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    REST_API = "rest_api"


class User(Base):
    """Users table"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    connections = relationship("Connection", back_populates="user", cascade="all, delete-orphan")
    request_logs = relationship("RequestLog", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_created_at", "created_at"),
    )


class APIKey(Base):
    """API Keys table"""
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="api_keys")
    request_logs = relationship("RequestLog", back_populates="api_key", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_api_keys_user_id", "user_id"),
        Index("ix_api_keys_created_at", "created_at"),
    )


class Connection(Base):
    """Connections table (data sources)"""
    __tablename__ = "connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum(ConnectionType), nullable=False)
    config = Column(JSON, nullable=False)  # Encrypted connection details
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="connections")

    __table_args__ = (
        Index("ix_connections_user_id", "user_id"),
        Index("ix_connections_created_at", "created_at"),
    )


class RequestLog(Base):
    """Request Logs table"""
    __tablename__ = "request_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey("api_keys.id"), nullable=True)
    request_type = Column(String(255), nullable=False)
    ai_provider = Column(String(255), nullable=False)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost = Column(Numeric(10, 6), default=0)
    latency_ms = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="request_logs")
    api_key = relationship("APIKey", back_populates="request_logs")

    __table_args__ = (
        Index("ix_request_logs_user_id", "user_id"),
        Index("ix_request_logs_api_key_id", "api_key_id"),
        Index("ix_request_logs_created_at", "created_at"),
    )
