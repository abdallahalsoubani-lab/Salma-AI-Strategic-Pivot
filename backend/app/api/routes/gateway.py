from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.schemas import (
    ChatRequest, ChatResponse, ProvidersListResponse, CostEstimate
)
from app.services.gateway_service import GatewayService
from app.api.dependencies import get_current_user_flexible
from app.db.session import get_db

router = APIRouter()
gateway_service = GatewayService()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint - send messages to AI providers
    """
    try:
        response = await gateway_service.process_request(
            user_id=current_user.id,
            messages=request.messages,
            provider=request.provider or "auto",
            model=request.model,
            context_sources=request.context_sources,
            options={}
        )

        return response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء معالجة الطلب"  # Error processing request
        )

@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Chat endpoint with streaming response (Server-Sent Events)
    """
    # Placeholder for streaming implementation
    return {"message": "Streaming will be implemented soon"}

@router.get("/providers", response_model=ProvidersListResponse)
async def get_providers(
    current_user: User = Depends(get_current_user_flexible)
):
    """
    Get list of available AI providers and their models
    """
    providers = gateway_service.get_providers()
    return ProvidersListResponse(providers=providers)

@router.post("/estimate", response_model=CostEstimate)
async def estimate_cost(
    request: ChatRequest,
    current_user: User = Depends(get_current_user_flexible),
    db: Session = Depends(get_db)
):
    """
    Estimate cost for a request before processing
    """
    try:
        estimate = await gateway_service.estimate_cost(
            messages=request.messages,
            provider=request.provider or "auto",
            model=request.model
        )

        return estimate

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="حدث خطأ أثناء حساب التكلفة"  # Error calculating cost
        )
