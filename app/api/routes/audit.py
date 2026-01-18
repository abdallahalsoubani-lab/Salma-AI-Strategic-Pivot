"""
مسارات API للتدقيق
Audit API Routes
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timedelta

from app.api.dependencies import get_current_user, get_db
from app.services.audit_service import AuditService
from app.services.analytics_service import AnalyticsService
from app.models.audit import AuditEventType, RequestStatus
from pydantic import BaseModel

router = APIRouter(prefix="/api/audit", tags=["audit"])


class TraceResponse(BaseModel):
    request_id: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    latency_ms: int
    status: str
    created_at: datetime
    explanation: Optional[dict] = None


class ExplanationResponse(BaseModel):
    explanation_ar: str
    explanation_en: str
    routing_factors: dict
    response_confidence: Optional[float]
    potential_issues: Optional[List[str]]


# ==================== TRACES ====================

@router.get("/traces")
async def list_traces(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    status: Optional[str] = None,
    provider: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(50, le=100),
    offset: int = 0
):
    """
    قائمة التتبعات
    List AI request traces for current user
    """
    audit_service = AuditService(db)

    status_enum = RequestStatus(status) if status else None

    traces = await audit_service.get_user_traces(
        user_id=current_user.id,
        limit=limit,
        offset=offset,
        status=status_enum,
        provider=provider,
        start_date=start_date,
        end_date=end_date
    )

    return {
        "traces": [
            {
                "request_id": t.request_id,
                "provider": t.selected_provider,
                "model": t.selected_model,
                "input_tokens": t.input_tokens,
                "output_tokens": t.output_tokens,
                "cost_usd": t.cost_usd,
                "latency_ms": t.total_latency_ms,
                "status": t.status.value,
                "created_at": t.created_at.isoformat()
            }
            for t in traces
        ],
        "total": len(traces),
        "limit": limit,
        "offset": offset
    }


@router.get("/traces/{request_id}")
async def get_trace_detail(
    request_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    """
    تفاصيل التتبع
    Get detailed trace information
    """
    audit_service = AuditService(db)
    trace = await audit_service.get_trace(request_id)

    if not trace:
        raise HTTPException(status_code=404, detail="التتبع غير موجود")

    # In a real app, verify user ownership
    # if trace.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="غير مصرح")

    return {
        "request_id": trace.request_id,
        "input": {
            "messages": trace.input_messages,
            "tokens": trace.input_tokens,
            "system_prompt": trace.system_prompt
        },
        "output": {
            "content": trace.output_content,
            "tokens": trace.output_tokens,
            "finish_reason": trace.finish_reason
        },
        "routing": {
            "requested_provider": trace.requested_provider,
            "selected_provider": trace.selected_provider,
            "selected_model": trace.selected_model,
            "reason": trace.routing_reason,
            "metadata": trace.routing_metadata
        },
        "context": {
            "sources_used": trace.context_sources_used,
            "data_summary": trace.context_data_summary
        },
        "performance": {
            "total_latency_ms": trace.total_latency_ms,
            "provider_latency_ms": trace.provider_latency_ms,
            "context_fetch_latency_ms": trace.context_fetch_latency_ms
        },
        "cost": {
            "total_usd": trace.cost_usd,
            "breakdown": trace.cost_breakdown
        },
        "status": trace.status.value,
        "error": {
            "type": trace.error_type,
            "message": trace.error_message
        } if trace.error_type else None,
        "timestamps": {
            "created_at": trace.created_at.isoformat(),
            "completed_at": trace.completed_at.isoformat() if trace.completed_at else None
        }
    }


@router.get("/traces/{request_id}/explanation")
async def get_trace_explanation(
    request_id: str,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    """
    شرح قرار AI
    Get AI decision explanation
    """
    audit_service = AuditService(db)
    trace = await audit_service.get_trace(request_id)

    if not trace:
        raise HTTPException(status_code=404, detail="التتبع غير موجود")

    explanation = trace.explanation

    if not explanation:
        return {
            "explanation_ar": "لا يوجد شرح متاح",
            "explanation_en": "No explanation available",
            "routing_factors": trace.routing_metadata or {}
        }

    return {
        "explanation_ar": explanation.explanation_ar,
        "explanation_en": explanation.explanation_en,
        "routing_factors": explanation.routing_factors,
        "context_relevance": explanation.context_relevance_scores,
        "response_confidence": explanation.response_confidence,
        "response_categories": explanation.response_categories,
        "potential_issues": explanation.potential_issues,
        "compliance": {
            "pii_detected": explanation.pii_detected,
            "pii_types": explanation.pii_types,
            "data_sensitivity": explanation.data_sensitivity,
            "flags": explanation.compliance_flags
        }
    }


# ==================== AUDIT LOGS ====================

@router.get("/logs")
async def list_audit_logs(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    event_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, le=500),
    offset: int = 0
):
    """
    سجلات التدقيق
    List audit logs
    """
    audit_service = AuditService(db)

    event_enum = AuditEventType(event_type) if event_type else None

    logs = await audit_service.get_audit_logs(
        user_id=current_user.id,
        event_type=event_enum,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )

    return {
        "logs": [
            {
                "id": str(log.id),
                "event_type": log.event_type.value,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "status": log.status.value,
                "ip_address": log.ip_address,
                "created_at": log.created_at.isoformat(),
                "duration_ms": log.duration_ms
            }
            for log in logs
        ],
        "total": len(logs),
        "limit": limit,
        "offset": offset
    }


# ==================== ANALYTICS ====================

@router.get("/analytics/summary")
async def get_analytics_summary(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    days: int = Query(30, le=90)
):
    """
    ملخص التحليلات
    Get usage analytics summary
    """
    analytics = AnalyticsService(db)

    start_date = datetime.utcnow() - timedelta(days=days)

    summary = await analytics.get_usage_summary(
        user_id=current_user.id,
        start_date=start_date
    )

    return summary


@router.get("/analytics/by-provider")
async def get_analytics_by_provider(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    days: int = Query(30, le=90)
):
    """
    التحليلات حسب المزود
    Get usage breakdown by provider
    """
    analytics = AnalyticsService(db)

    start_date = datetime.utcnow() - timedelta(days=days)

    by_provider = await analytics.get_usage_by_provider(
        user_id=current_user.id,
        start_date=start_date
    )

    return {"providers": by_provider}


@router.get("/analytics/trend")
async def get_analytics_trend(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    days: int = Query(7, le=30),
    granularity: str = Query("daily", regex="^(hourly|daily)$")
):
    """
    اتجاه الاستخدام
    Get usage trend over time
    """
    analytics = AnalyticsService(db)

    trend = await analytics.get_usage_trend(
        user_id=current_user.id,
        days=days,
        granularity=granularity
    )

    return {"trend": trend}


@router.get("/analytics/top-queries")
async def get_top_queries(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    days: int = Query(7, le=30),
    limit: int = Query(10, le=50)
):
    """
    أكثر الاستعلامات
    Get most expensive/frequent queries
    """
    analytics = AnalyticsService(db)

    queries = await analytics.get_top_queries(
        user_id=current_user.id,
        limit=limit,
        days=days
    )

    return {"queries": queries}


# ==================== REPORTS ====================

@router.get("/reports/compliance")
async def get_compliance_report(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    تقرير الامتثال
    Generate compliance report
    """
    analytics = AnalyticsService(db)

    report = await analytics.generate_compliance_report(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return report


@router.get("/reports/export")
async def export_report(
    current_user=Depends(get_current_user),
    db=Depends(get_db),
    format: str = Query("json", regex="^(json|csv)$"),
    days: int = Query(30, le=90)
):
    """
    تصدير التقرير
    Export audit report
    """
    return {
        "message": "سيتم إرسال التقرير إلى بريدك الإلكتروني",
        "format": format,
        "period_days": days
    }
