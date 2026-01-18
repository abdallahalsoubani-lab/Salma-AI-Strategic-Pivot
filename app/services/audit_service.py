"""
خدمة التدقيق
Audit Service - Handles all audit logging and tracing
"""

from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.models.audit import (
    AuditLog, AIRequestTrace, AIExplanation, UsageMetrics,
    AuditEventType, RequestStatus
)


class AuditService:
    """خدمة التدقيق والتتبع"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== AUDIT LOGGING ====================

    async def log_event(
        self,
        event_type: AuditEventType,
        action: str,
        user_id: Optional[UUID] = None,
        api_key_id: Optional[UUID] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        request_data: Optional[Dict] = None,
        response_summary: Optional[Dict] = None,
        status: RequestStatus = RequestStatus.SUCCESS,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> AuditLog:
        """
        تسجيل حدث في سجل التدقيق
        Log an event to the audit log
        """

        sanitized_request = self._sanitize_data(request_data) if request_data else None

        audit_log = AuditLog(
            user_id=user_id,
            api_key_id=api_key_id,
            event_type=event_type,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            request_data=sanitized_request,
            response_summary=response_summary,
            status=status,
            error_message=error_message,
            duration_ms=duration_ms,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata
        )

        self.db.add(audit_log)
        await self.db.commit()
        await self.db.refresh(audit_log)

        return audit_log

    def _sanitize_data(self, data: Dict) -> Dict:
        """إزالة البيانات الحساسة"""
        sensitive_keys = ['password', 'api_key', 'token', 'secret', 'credential']
        sanitized = {}

        for key, value in data.items():
            if any(s in key.lower() for s in sensitive_keys):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_data(value)
            else:
                sanitized[key] = value

        return sanitized

    # ==================== AI REQUEST TRACING ====================

    async def create_trace(
        self,
        request_id: str,
        user_id: UUID,
        input_messages: List[Dict],
        selected_provider: str,
        selected_model: str,
        api_key_id: Optional[UUID] = None,
        requested_provider: Optional[str] = None,
        routing_reason: Optional[str] = None,
        routing_metadata: Optional[Dict] = None,
        system_prompt: Optional[str] = None,
        context_sources_used: Optional[List[str]] = None
    ) -> AIRequestTrace:
        """
        إنشاء تتبع لطلب AI
        Create a trace for an AI request
        """

        input_tokens = sum(
            len(msg.get('content', '')) // 4
            for msg in input_messages
        )

        trace = AIRequestTrace(
            request_id=request_id,
            user_id=user_id,
            api_key_id=api_key_id,
            input_messages=input_messages,
            input_tokens=input_tokens,
            system_prompt=system_prompt,
            requested_provider=requested_provider,
            selected_provider=selected_provider,
            selected_model=selected_model,
            routing_reason=routing_reason,
            routing_metadata=routing_metadata,
            context_sources_used=context_sources_used,
            status=RequestStatus.PENDING
        )

        self.db.add(trace)
        await self.db.commit()
        await self.db.refresh(trace)

        return trace

    async def complete_trace(
        self,
        request_id: str,
        output_content: str,
        output_tokens: int,
        cost_usd: float,
        total_latency_ms: int,
        provider_latency_ms: Optional[int] = None,
        finish_reason: Optional[str] = None,
        cost_breakdown: Optional[Dict] = None,
        status: RequestStatus = RequestStatus.SUCCESS,
        error_type: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> AIRequestTrace:
        """
        إكمال تتبع الطلب
        Complete the trace with response details
        """

        result = await self.db.execute(
            select(AIRequestTrace).where(AIRequestTrace.request_id == request_id)
        )
        trace = result.scalar_one_or_none()

        if not trace:
            raise ValueError(f"Trace not found: {request_id}")

        trace.output_content = output_content
        trace.output_tokens = output_tokens
        trace.cost_usd = cost_usd
        trace.total_latency_ms = total_latency_ms
        trace.provider_latency_ms = provider_latency_ms
        trace.finish_reason = finish_reason
        trace.cost_breakdown = cost_breakdown
        trace.status = status
        trace.error_type = error_type
        trace.error_message = error_message
        trace.completed_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(trace)

        return trace

    # ==================== EXPLAINABILITY ====================

    async def create_explanation(
        self,
        trace_id: UUID,
        routing_factors: Dict,
        explanation_ar: Optional[str] = None,
        explanation_en: Optional[str] = None,
        context_relevance_scores: Optional[Dict] = None,
        response_confidence: Optional[float] = None,
        response_categories: Optional[List[str]] = None,
        potential_issues: Optional[List[str]] = None,
        pii_detected: bool = False,
        pii_types: Optional[List[str]] = None,
        data_sensitivity: Optional[str] = None,
        compliance_flags: Optional[List[str]] = None
    ) -> AIExplanation:
        """
        إنشاء شرح لقرار AI
        Create explanation for AI decision
        """

        if not explanation_ar:
            explanation_ar = self._generate_explanation_ar(routing_factors)
        if not explanation_en:
            explanation_en = self._generate_explanation_en(routing_factors)

        explanation = AIExplanation(
            trace_id=trace_id,
            explanation_ar=explanation_ar,
            explanation_en=explanation_en,
            routing_factors=routing_factors,
            context_relevance_scores=context_relevance_scores,
            response_confidence=response_confidence,
            response_categories=response_categories,
            potential_issues=potential_issues,
            pii_detected=pii_detected,
            pii_types=pii_types,
            data_sensitivity=data_sensitivity,
            compliance_flags=compliance_flags
        )

        self.db.add(explanation)
        await self.db.commit()
        await self.db.refresh(explanation)

        return explanation

    def _generate_explanation_ar(self, factors: Dict) -> str:
        """توليد شرح بالعربية"""
        parts = []

        lang = factors.get('language_detected', 'en')
        if lang == 'ar':
            parts.append("تم اكتشاف أن الاستعلام باللغة العربية")

        provider = factors.get('selected_provider')
        if provider == 'jais':
            parts.append("تم اختيار نموذج جيس لأنه الأفضل للغة العربية")
        elif provider == 'claude':
            parts.append("تم اختيار كلود لتوازنه بين الجودة والتكلفة")

        complexity = factors.get('complexity_score', 0)
        if complexity > 0.7:
            parts.append("الاستعلام معقد ويتطلب نموذجاً متقدماً")
        elif complexity < 0.3:
            parts.append("الاستعلام بسيط ويمكن معالجته بنموذج سريع")

        return ". ".join(parts) + "." if parts else "تم التوجيه تلقائياً."

    def _generate_explanation_en(self, factors: Dict) -> str:
        """Generate English explanation"""
        parts = []

        lang = factors.get('language_detected', 'en')
        if lang == 'ar':
            parts.append("Query detected as Arabic language")

        provider = factors.get('selected_provider')
        if provider == 'jais':
            parts.append("Jais selected for optimal Arabic performance")
        elif provider == 'claude':
            parts.append("Claude selected for quality-cost balance")

        complexity = factors.get('complexity_score', 0)
        if complexity > 0.7:
            parts.append("Complex query requiring advanced model")
        elif complexity < 0.3:
            parts.append("Simple query suitable for fast model")

        return ". ".join(parts) + "." if parts else "Auto-routed based on default rules."

    # ==================== QUERIES ====================

    async def get_trace(self, request_id: str) -> Optional[AIRequestTrace]:
        """الحصول على تتبع بالـ ID"""
        result = await self.db.execute(
            select(AIRequestTrace).where(AIRequestTrace.request_id == request_id)
        )
        return result.scalar_one_or_none()

    async def get_user_traces(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
        status: Optional[RequestStatus] = None,
        provider: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AIRequestTrace]:
        """الحصول على تتبعات المستخدم"""
        query = select(AIRequestTrace).where(AIRequestTrace.user_id == user_id)

        if status:
            query = query.where(AIRequestTrace.status == status)
        if provider:
            query = query.where(AIRequestTrace.selected_provider == provider)
        if start_date:
            query = query.where(AIRequestTrace.created_at >= start_date)
        if end_date:
            query = query.where(AIRequestTrace.created_at <= end_date)

        query = query.order_by(AIRequestTrace.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_audit_logs(
        self,
        user_id: Optional[UUID] = None,
        event_type: Optional[AuditEventType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[AuditLog]:
        """الحصول على سجلات التدقيق"""
        query = select(AuditLog)

        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if event_type:
            query = query.where(AuditLog.event_type == event_type)
        if start_date:
            query = query.where(AuditLog.created_at >= start_date)
        if end_date:
            query = query.where(AuditLog.created_at <= end_date)

        query = query.order_by(AuditLog.created_at.desc())
        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()
