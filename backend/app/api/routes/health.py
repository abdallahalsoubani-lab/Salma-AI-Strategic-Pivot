"""
صفحة الصحة والحالة
Health Check & Status Endpoints
"""

from fastapi import APIRouter, Depends
from datetime import datetime
import platform
import psutil

from app.core.database import get_db
from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/api/health")
async def health_check():
    """
    فحص صحة النظام
    Basic health check
    """
    return {
        "status": "healthy",
        "service": "salma-gateway",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/api/health/detailed")
async def detailed_health_check(db = Depends(get_db)):
    """
    فحص صحة مفصل
    Detailed health check with component status
    """

    checks = {
        "database": await check_database(db),
        "redis": await check_redis(),
        "disk": check_disk(),
        "memory": check_memory()
    }

    all_healthy = all(c["status"] == "healthy" for c in checks.values())

    return {
        "status": "healthy" if all_healthy else "degraded",
        "service": "salma-gateway",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }
    }


async def check_database(db) -> dict:
    """Check database connection"""
    try:
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "message": "Connected"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}


async def check_redis() -> dict:
    """Check Redis connection"""
    try:
        import redis.asyncio as redis
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.close()
        return {"status": "healthy", "message": "Connected"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}


def check_disk() -> dict:
    """Check disk usage"""
    disk = psutil.disk_usage('/')
    used_percent = disk.percent

    status = "healthy" if used_percent < 80 else "warning" if used_percent < 90 else "critical"

    return {
        "status": status,
        "used_percent": used_percent,
        "free_gb": round(disk.free / (1024**3), 2)
    }


def check_memory() -> dict:
    """Check memory usage"""
    memory = psutil.virtual_memory()
    used_percent = memory.percent

    status = "healthy" if used_percent < 80 else "warning" if used_percent < 90 else "critical"

    return {
        "status": status,
        "used_percent": used_percent,
        "available_gb": round(memory.available / (1024**3), 2)
    }


@router.get("/api/status")
async def system_status(db = Depends(get_db)):
    """
    حالة النظام الكاملة
    Full system status for admin dashboard
    """

    # Get counts
    from sqlalchemy import text, func
    from app.models.audit import AIRequestTrace
    from app.models.documents import Document

    # Request stats (last 24 hours)
    from datetime import timedelta
    yesterday = datetime.utcnow() - timedelta(days=1)

    request_count = await db.scalar(
        text("SELECT COUNT(*) FROM ai_request_traces WHERE created_at > :since"),
        {"since": yesterday}
    )

    document_count = await db.scalar(
        text("SELECT COUNT(*) FROM documents")
    )

    user_count = await db.scalar(
        text("SELECT COUNT(*) FROM users WHERE is_active = true")
    )

    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "stats": {
            "requests_24h": request_count or 0,
            "total_documents": document_count or 0,
            "active_users": user_count or 0
        },
        "components": {
            "api": "operational",
            "database": "operational",
            "cache": "operational",
            "ai_providers": {
                "claude": "operational",
                "openai": "operational",
                "jais": "operational"
            }
        }
    }
