from typing import List, Optional
from datetime import datetime, timezone
from decimal import Decimal
import uuid
import logging
from app.models.schemas import (
    Message, ChatResponse, UsageInfo, CostEstimate,
    ProviderInfo, ProviderModel
)

logger = logging.getLogger(__name__)

class GatewayService:
    """
    Core MCP-like gateway that routes requests to AI providers
    """

    # Provider configurations
    PROVIDERS = {
        "claude": {
            "name": "Claude (Anthropic)",
            "name_ar": "كلود (Anthropic)",
            "status": "active",
            "models": [
                {
                    "id": "claude-3-5-sonnet-20241022",
                    "name": "Claude 3.5 Sonnet",
                    "name_ar": "كلود 3.5 سونيت",
                    "max_tokens": 200000,
                    "cost_per_1k_input": Decimal("0.003"),
                    "cost_per_1k_output": Decimal("0.015")
                },
                {
                    "id": "claude-opus-4-1-20250805",
                    "name": "Claude Opus 4.1",
                    "name_ar": "كلود أوبس 4.1",
                    "max_tokens": 200000,
                    "cost_per_1k_input": Decimal("0.015"),
                    "cost_per_1k_output": Decimal("0.075")
                }
            ]
        },
        "openai": {
            "name": "OpenAI",
            "name_ar": "أوبن أي آي",
            "status": "active",
            "models": [
                {
                    "id": "gpt-4-turbo",
                    "name": "GPT-4 Turbo",
                    "name_ar": "جي بي تي 4 توربو",
                    "max_tokens": 128000,
                    "cost_per_1k_input": Decimal("0.01"),
                    "cost_per_1k_output": Decimal("0.03")
                },
                {
                    "id": "gpt-4o",
                    "name": "GPT-4o",
                    "name_ar": "جي بي تي 4 أو",
                    "max_tokens": 128000,
                    "cost_per_1k_input": Decimal("0.005"),
                    "cost_per_1k_output": Decimal("0.015")
                }
            ]
        },
        "jais": {
            "name": "Jais (G42)",
            "name_ar": "جايس (جي 42)",
            "status": "coming_soon",
            "models": [
                {
                    "id": "jais-30b-chat",
                    "name": "Jais 30B Chat",
                    "name_ar": "جايس 30 بي تشات",
                    "max_tokens": 8192,
                    "cost_per_1k_input": Decimal("0.002"),
                    "cost_per_1k_output": Decimal("0.005")
                }
            ]
        }
    }

    async def process_request(
        self,
        user_id: str,
        messages: List[Message],
        provider: str = "auto",
        model: Optional[str] = None,
        context_sources: Optional[List[str]] = None,
        options: Optional[dict] = None
    ) -> ChatResponse:
        """
        Main gateway method:
        1. Validate user and permissions
        2. If context_sources provided, fetch context from data connections
        3. Route to appropriate AI provider
        4. Log request and response
        5. Return unified response
        """
        if not messages:
            raise ValueError("At least one message is required")

        # Select provider if auto
        if provider == "auto":
            provider = "claude"

        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")

        # Select model
        if not model:
            model = self.PROVIDERS[provider]["models"][0]["id"]

        # For now, return a mock response
        # In production, this would call the actual AI provider
        start_time = datetime.now(timezone.utc)

        response_text = f"Mock response from {provider} using {model}. " \
                       f"Received {len(messages)} messages."

        end_time = datetime.now(timezone.utc)
        latency_ms = int((end_time - start_time).total_seconds() * 1000)

        # Estimate tokens (simplified)
        input_tokens = sum(len(msg.content.split()) for msg in messages) * 2
        output_tokens = len(response_text.split()) * 2

        # Get cost info
        provider_info = self.PROVIDERS[provider]
        model_info = next(
            (m for m in provider_info["models"] if m["id"] == model),
            provider_info["models"][0]
        )

        cost = (
            Decimal(input_tokens) / 1000 * model_info["cost_per_1k_input"] +
            Decimal(output_tokens) / 1000 * model_info["cost_per_1k_output"]
        )

        return ChatResponse(
            id=f"req_{uuid.uuid4().hex[:8]}",
            response=response_text,
            provider=provider,
            model=model,
            usage=UsageInfo(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost
            ),
            latency_ms=latency_ms,
            created_at=start_time
        )

    async def estimate_cost(
        self,
        messages: List[Message],
        provider: str,
        model: Optional[str] = None
    ) -> CostEstimate:
        """Estimate cost before processing"""
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")

        if not model:
            model = self.PROVIDERS[provider]["models"][0]["id"]

        model_info = next(
            (m for m in self.PROVIDERS[provider]["models"] if m["id"] == model),
            self.PROVIDERS[provider]["models"][0]
        )

        # Estimate tokens
        estimated_tokens = sum(len(msg.content.split()) for msg in messages) * 2

        # Assume response is roughly same size as input
        estimated_tokens *= 2

        cost = (
            Decimal(estimated_tokens) / 1000 * model_info["cost_per_1k_input"] +
            Decimal(estimated_tokens) / 1000 * model_info["cost_per_1k_output"]
        ) / 2

        return CostEstimate(
            estimated_cost=cost,
            provider=provider,
            model=model,
            estimated_tokens=estimated_tokens
        )

    def get_providers(self) -> List[ProviderInfo]:
        """Get list of available providers"""
        providers = []

        for provider_id, provider_data in self.PROVIDERS.items():
            models = [
                ProviderModel(
                    id=m["id"],
                    name=m["name"],
                    name_ar=m["name_ar"],
                    max_tokens=m["max_tokens"],
                    cost_per_1k_input=m["cost_per_1k_input"],
                    cost_per_1k_output=m["cost_per_1k_output"]
                )
                for m in provider_data["models"]
            ]

            providers.append(
                ProviderInfo(
                    id=provider_id,
                    name=provider_data["name"],
                    name_ar=provider_data["name_ar"],
                    status=provider_data["status"],
                    models=models
                )
            )

        return providers
