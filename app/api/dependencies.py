"""
API Dependencies
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal


async def get_db() -> AsyncSession:
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(db: AsyncSession = Depends(get_db)):
    """Get current user (mock implementation)"""
    # In a real implementation, this would verify JWT tokens
    class CurrentUser:
        id = None
        email = "test@example.com"
        is_active = True

    return CurrentUser()
