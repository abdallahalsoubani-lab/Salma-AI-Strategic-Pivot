from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import logging

from app.db.session import get_db
from app.models.user import User, AuthLog
from app.models.schemas import (
    UserCreate, LoginRequest, LoginResponse, RegisterResponse,
    RefreshTokenRequest, TokenResponse, User as UserSchema, UserUpdate
)
from app.core.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, verify_token
)
from app.api.dependencies import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

def log_auth_event(
    db: Session,
    action: str,
    email: str = None,
    user_id: str = None,
    success: bool = True
):
    """Log authentication events"""
    log_entry = AuthLog(
        user_id=user_id,
        email=email,
        action=action,
        success=success
    )
    db.add(log_entry)
    db.commit()

@router.post("/register", response_model=RegisterResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        log_auth_event(db, "register_failed", user_data.email, success=False)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مسجل بالفعل"  # Email already registered
        )

    # Validate password strength
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="كلمة المرور يجب أن تكون 8 أحرف على الأقل"  # Password must be at least 8 characters
        )

    # Create new user
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        organization=user_data.organization,
        hashed_password=hash_password(user_data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    log_auth_event(db, "register", user_data.email, user.id)

    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return RegisterResponse(
        user=UserSchema.from_orm(user),
        access_token=access_token,
    )

@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user and return tokens"""
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        log_auth_event(db, "login_failed", credentials.email, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة"  # Invalid email or password
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="حسابك معطل"  # Your account is disabled
        )

    # Update last login
    user.last_login = datetime.now(timezone.utc)
    db.commit()

    log_auth_event(db, "login", credentials.email, user.id)

    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserSchema.from_orm(user)
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    user_id = verify_token(request.refresh_token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    access_token = create_access_token(user.id)

    return TokenResponse(access_token=access_token)

@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout user (log the event)"""
    log_auth_event(db, "logout", current_user.email, current_user.id)
    return {"message": "تم تسجيل الخروج بنجاح"}  # Successfully logged out

@router.get("/me", response_model=UserSchema)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return UserSchema.from_orm(current_user)

@router.put("/me", response_model=UserSchema)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if user_update.full_name:
        current_user.full_name = user_update.full_name

    if user_update.organization:
        current_user.organization = user_update.organization

    current_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)

    return UserSchema.from_orm(current_user)
