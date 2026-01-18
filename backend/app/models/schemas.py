from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Literal
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Auth Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    organization: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    organization: Optional[str] = None

class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User

class RegisterResponse(BaseModel):
    user: User
    access_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# API Key Schemas
class APIKeyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    expires_at: Optional[datetime] = None

class APIKeyResponse(BaseModel):
    id: str
    name: str
    key_hash: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class APIKeyCreateResponse(BaseModel):
    id: str
    name: str
    key: str  # Full key shown only on creation
    created_at: datetime
    warning: str = "Please save this key now. You won't be able to see it again!"

class APIKeyListResponse(BaseModel):
    id: str
    name: str
    masked_key: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class APIKeyUsageStats(BaseModel):
    key_id: str
    name: str
    total_requests: int
    last_used_at: Optional[datetime]
    created_at: datetime

# Gateway Schemas
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    provider: Optional[str] = "auto"
    model: Optional[str] = None
    context_sources: Optional[List[str]] = None
    stream: Optional[bool] = False

class UsageInfo(BaseModel):
    input_tokens: int
    output_tokens: int
    cost: Decimal

class ChatResponse(BaseModel):
    id: str
    response: str
    provider: str
    model: str
    usage: UsageInfo
    latency_ms: int
    created_at: datetime

class ProviderModel(BaseModel):
    id: str
    name: str
    name_ar: str
    max_tokens: int
    cost_per_1k_input: Decimal
    cost_per_1k_output: Decimal

class ProviderInfo(BaseModel):
    id: str
    name: str
    name_ar: str
    status: Literal["active", "inactive", "coming_soon"]
    models: List[ProviderModel]

class ProvidersListResponse(BaseModel):
    providers: List[ProviderInfo]

class CostEstimate(BaseModel):
    estimated_cost: Decimal
    provider: str
    model: str
    estimated_tokens: int

# Error Schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
