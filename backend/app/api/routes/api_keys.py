from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from app.db.session import get_db
from app.models.user import User, APIKey
from app.models.schemas import (
    APIKeyCreate, APIKeyCreateResponse, APIKeyListResponse, APIKeyUsageStats
)
from app.core.security import generate_api_key, hash_api_key, mask_api_key
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("", response_model=APIKeyCreateResponse)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new API key for the current user"""
    # Generate new key
    raw_key = generate_api_key()
    key_hash = hash_api_key(raw_key)

    # Create API key record
    api_key = APIKey(
        user_id=current_user.id,
        name=key_data.name,
        key_hash=key_hash,
        expires_at=key_data.expires_at
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return APIKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        key=raw_key,
        created_at=api_key.created_at,
        warning="احفظ هذا المفتاح الآن. لن تتمكن من رؤيته مرة أخرى!"  # Save this key now. You won't see it again!
    )

@router.get("", response_model=List[APIKeyListResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all API keys for the current user"""
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.id).all()

    response = []
    for key in api_keys:
        response.append(
            APIKeyListResponse(
                id=key.id,
                name=key.name,
                masked_key=mask_api_key(key.key_hash),
                is_active=key.is_active,
                created_at=key.created_at,
                last_used_at=key.last_used_at
            )
        )

    return response

@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deactivate an API key"""
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="مفتاح API غير موجود"  # API key not found
        )

    api_key.is_active = False
    db.commit()

    return {"message": "تم حذف المفتاح بنجاح"}  # Key deleted successfully

@router.get("/{key_id}/usage", response_model=APIKeyUsageStats)
async def get_api_key_usage(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get usage stats for a specific API key"""
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.user_id == current_user.id
    ).first()

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="مفتاح API غير موجود"  # API key not found
        )

    return APIKeyUsageStats(
        key_id=api_key.id,
        name=api_key.name,
        total_requests=0,  # Will be updated when we add request logging
        last_used_at=api_key.last_used_at,
        created_at=api_key.created_at
    )
