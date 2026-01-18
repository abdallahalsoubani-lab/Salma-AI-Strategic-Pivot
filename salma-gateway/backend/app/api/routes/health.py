"""Health check endpoints"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.config import get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Health check endpoint
    Returns status of API and database connection
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception as e:
        database_status = f"disconnected: {str(e)}"

    return {
        "status": "healthy",
        "service": "salma-gateway",
        "version": settings.APP_VERSION,
        "database": database_status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
