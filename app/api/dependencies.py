"""API Dependencies"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import async_session
from app.models.documents import Document


security = HTTPBearer()


async def get_db() -> AsyncSession:
    """Get database session"""
    async with async_session() as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
) -> Optional[dict]:
    """
    Get current authenticated user
    In production, verify JWT token here
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # TODO: Verify JWT token and return user
    return {"id": "user_id"}
