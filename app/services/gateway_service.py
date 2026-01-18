"""Main Gateway Service for processing AI requests"""
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from app.connectors.ai import smart_router, AIMessage
from app.models.schemas import ChatRequest, ChatResponse, UsageInfo
from app.core.database import get_db
from app.models.database import RequestLog


class GatewayService:
    """Main gateway service that handles all AI requests"""

    async def process_chat(
        self,
        user_id: UUID,
        api_key_id: Optional[UUID],
        request: ChatRequest
    ) -> ChatResponse:
        """Process a chat request through the gateway"""

        start_time = datetime.utcnow()

        # Convert to AI messages
        ai_messages = [
            AIMessage(role=msg.role, content=msg.content)
            for msg in request.messages
        ]

        # Route and execute
        response, routing_info = await smart_router.route_and_execute(
            messages=ai_messages,
            preferred_provider=request.provider if request.provider != "auto" else None,
            preferred_model=request.model,
            routing_strategy="auto",
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            system_prompt=request.system_prompt
        )

        # Calculate latency
        latency_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        # Log request
        await self._log_request(
            user_id=user_id,
            api_key_id=api_key_id,
            provider=routing_info["selected_provider"],
            model=routing_info["selected_model"],
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            cost=routing_info["cost_usd"],
            latency_ms=latency_ms,
            status="success"
        )

        return ChatResponse(
            id=f"req_{uuid4().hex[:12]}",
            response=response.content,
            provider=response.provider,
            model=response.model,
            usage=UsageInfo(
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                cost=Decimal(str(routing_info["cost_usd"]))
            ),
            latency_ms=latency_ms,
            created_at=datetime.utcnow()
        )

    async def _log_request(
        self,
        user_id: UUID,
        api_key_id: Optional[UUID],
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        latency_ms: int,
        status: str
    ):
        """Log request to database"""
        # Implementation to save to RequestLog table
        # This would be implemented when database integration is set up
        pass

    def get_providers(self) -> List[dict]:
        """Get all available providers"""
        return smart_router.get_all_providers_status()


# Global instance
gateway_service = GatewayService()
