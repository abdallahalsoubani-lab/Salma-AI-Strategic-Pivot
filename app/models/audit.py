"""
نماذج قاعدة بيانات التدقيق
Audit Database Models
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class AuditEventType(str, enum.Enum):
    """أنواع أحداث التدقيق"""
    CHAT_REQUEST = "chat_request"
    CHAT_RESPONSE = "chat_response"
    DATA_QUERY = "data_query"
    CONNECTION_CREATE = "connection_create"
    CONNECTION_DELETE = "connection_delete"
    API_KEY_CREATE = "api_key_create"
    API_KEY_DELETE = "api_key_delete"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    SETTINGS_CHANGE = "settings_change"
    ERROR = "error"


class RequestStatus(str, enum.Enum):
    """حالة الطلب"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    BLOCKED = "blocked"


class AuditLog(Base):
    """
    سجل التدقيق الرئيسي
    Main Audit Log - stores every significant action
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Who
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    api_key_id = Column(UUID(as_uuid=True), nullable=True)
    session_id = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)

    # What
    event_type = Column(Enum(AuditEventType), nullable=False)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(String(100), nullable=True)

    # Details
    request_data = Column(JSON, nullable=True)
    response_summary = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)

    # Result
    status = Column(Enum(RequestStatus), default=RequestStatus.SUCCESS)
    error_message = Column(Text, nullable=True)

    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    duration_ms = Column(Integer, nullable=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.event_type}:{self.action} at {self.created_at}>"


class AIRequestTrace(Base):
    """
    تتبع طلبات الذكاء الاصطناعي
    Detailed trace of AI requests for explainability
    """
    __tablename__ = "ai_request_traces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(String(50), unique=True, nullable=False)

    # Link to audit
    audit_log_id = Column(UUID(as_uuid=True), nullable=True)

    # User context
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    api_key_id = Column(UUID(as_uuid=True), nullable=True)

    # Request details
    input_messages = Column(JSON, nullable=False)
    input_tokens = Column(Integer, default=0)
    system_prompt = Column(Text, nullable=True)

    # Routing decision
    requested_provider = Column(String(50), nullable=True)
    selected_provider = Column(String(50), nullable=False)
    selected_model = Column(String(100), nullable=False)
    routing_reason = Column(String(200), nullable=True)
    routing_metadata = Column(JSON, nullable=True)

    # Context sources
    context_sources_used = Column(JSON, nullable=True)
    context_data_summary = Column(JSON, nullable=True)

    # Response details
    output_content = Column(Text, nullable=True)
    output_tokens = Column(Integer, default=0)
    finish_reason = Column(String(50), nullable=True)

    # Cost tracking
    cost_usd = Column(Float, default=0.0)
    cost_breakdown = Column(JSON, nullable=True)

    # Performance
    total_latency_ms = Column(Integer, nullable=True)
    provider_latency_ms = Column(Integer, nullable=True)
    context_fetch_latency_ms = Column(Integer, nullable=True)

    # Status
    status = Column(Enum(RequestStatus), default=RequestStatus.SUCCESS)
    error_type = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Explainability
    explanation = relationship("AIExplanation", back_populates="trace", uselist=False)

    def __repr__(self):
        return f"<AIRequestTrace {self.request_id} - {self.selected_provider}>"


class AIExplanation(Base):
    """
    شرح قرارات الذكاء الاصطناعي
    Explainability data for AI decisions
    """
    __tablename__ = "ai_explanations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trace_id = Column(UUID(as_uuid=True), ForeignKey("ai_request_traces.id"), nullable=False)

    # Human-readable explanation
    explanation_ar = Column(Text, nullable=True)
    explanation_en = Column(Text, nullable=True)

    # Decision factors
    routing_factors = Column(JSON, nullable=True)

    # Context relevance
    context_relevance_scores = Column(JSON, nullable=True)

    # Response analysis
    response_confidence = Column(Float, nullable=True)
    response_categories = Column(JSON, nullable=True)
    potential_issues = Column(JSON, nullable=True)

    # Compliance
    pii_detected = Column(Boolean, default=False)
    pii_types = Column(JSON, nullable=True)
    data_sensitivity = Column(String(20), nullable=True)
    compliance_flags = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    trace = relationship("AIRequestTrace", back_populates="explanation")


class UsageMetrics(Base):
    """
    مقاييس الاستخدام المجمعة
    Aggregated usage metrics for reporting
    """
    __tablename__ = "usage_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Aggregation period
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    period_type = Column(String(20), nullable=False)

    # Scope
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    provider = Column(String(50), nullable=True)

    # Metrics
    total_requests = Column(Integer, default=0)
    successful_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)

    total_input_tokens = Column(Integer, default=0)
    total_output_tokens = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)

    avg_latency_ms = Column(Float, nullable=True)
    p95_latency_ms = Column(Float, nullable=True)
    p99_latency_ms = Column(Float, nullable=True)

    # Breakdown
    requests_by_provider = Column(JSON, nullable=True)
    cost_by_provider = Column(JSON, nullable=True)
    requests_by_status = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
