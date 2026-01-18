"""Pydantic schemas for API requests and responses"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class Message(BaseModel):
    """Message in conversation"""
    role: str = Field(..., description="user, assistant, or system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request to chat endpoint"""
    messages: List[Message] = Field(..., description="Conversation messages")
    provider: str = Field(default="auto", description="AI provider: auto, claude, openai, jais")
    model: Optional[str] = Field(default=None, description="Specific model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=8192)
    system_prompt: Optional[str] = Field(default=None, description="System prompt")


class UsageInfo(BaseModel):
    """Token usage information"""
    input_tokens: int
    output_tokens: int
    cost: Decimal = Field(description="Cost in USD")


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    id: str = Field(description="Request ID")
    response: str = Field(description="AI response content")
    provider: str = Field(description="Provider used")
    model: str = Field(description="Model used")
    usage: UsageInfo
    latency_ms: int = Field(description="Request latency in milliseconds")
    created_at: datetime


class ProvidersResponse(BaseModel):
    """Response listing all providers"""
    providers: List[dict]
