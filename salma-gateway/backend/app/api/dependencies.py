"""API dependency injection"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db


async def verify_database_connection(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    """Verify database is accessible"""
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection unavailable",
        )
    return db
