"""Anthropic Claude API Connector"""
import httpx
import json
from typing import List, Optional, AsyncIterator
from app.config import settings
from .base import AIProviderBase, AIMessage, AIResponse


class ClaudeConnector(AIProviderBase):
    """Anthropic Claude API Connector"""

    provider_id = "claude"
    provider_name = "Claude (Anthropic)"
    provider_name_ar = "كلود (أنثروبيك)"

    API_URL = "https://api.anthropic.com/v1/messages"

    MODELS = {
        "claude-sonnet-4-20250514": {
            "name": "Claude Sonnet 4",
            "name_ar": "كلود سونيت 4",
            "input_price": 3.0,    # per 1M tokens
            "output_price": 15.0,  # per 1M tokens
            "max_tokens": 8192,
            "context_window": 200000,
            "tier": "balanced"     # fast, balanced, powerful
        },
        "claude-haiku-3-5-20241022": {
            "name": "Claude Haiku 3.5",
            "name_ar": "كلود هايكو 3.5",
            "input_price": 0.80,
            "output_price": 4.0,
            "max_tokens": 8192,
            "context_window": 200000,
            "tier": "fast"
        },
        "claude-opus-4-20250514": {
            "name": "Claude Opus 4",
            "name_ar": "كلود أوبوس 4",
            "input_price": 15.0,
            "output_price": 75.0,
            "max_tokens": 8192,
            "context_window": 200000,
            "tier": "powerful"
        }
    }

    DEFAULT_MODEL = "claude-sonnet-4-20250514"

    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.client = httpx.AsyncClient(
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            timeout=120.0
        )

    async def chat(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Send chat request to Claude API"""

        model = model or self.DEFAULT_MODEL

        # Prepare messages (separate system from user/assistant)
        api_messages = []
        system = system_prompt or ""

        for msg in messages:
            if msg.role == "system":
                system += "\n" + msg.content if system else msg.content
            else:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": api_messages
        }

        if system:
            payload["system"] = system

        response = await self.client.post(self.API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        return AIResponse(
            content=data["content"][0]["text"],
            model=data["model"],
            provider=self.provider_id,
            input_tokens=data["usage"]["input_tokens"],
            output_tokens=data["usage"]["output_tokens"],
            finish_reason=data["stop_reason"]
        )

    async def chat_stream(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream chat response from Claude API"""

        model = model or self.DEFAULT_MODEL

        api_messages = []
        system = system_prompt or ""

        for msg in messages:
            if msg.role == "system":
                system += "\n" + msg.content if system else msg.content
            else:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": api_messages,
            "stream": True
        }

        if system:
            payload["system"] = system

        async with self.client.stream("POST", self.API_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    # Parse SSE data and yield content
                    try:
                        data = json.loads(line[6:])
                        if data.get("type") == "content_block_delta":
                            yield data["delta"]["text"]
                    except json.JSONDecodeError:
                        pass

    def get_available_models(self) -> List[dict]:
        """Return list of available models with pricing"""
        return [
            {
                "id": model_id,
                "name": info["name"],
                "name_ar": info["name_ar"],
                "tier": info["tier"],
                "input_price": info["input_price"],
                "output_price": info["output_price"],
                "context_window": info["context_window"]
            }
            for model_id, info in self.MODELS.items()
        ]

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        # Rough estimation: ~4 chars per token for English, ~2 for Arabic
        return len(text) // 3

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost in USD"""
        model_info = self.MODELS.get(model, self.MODELS[self.DEFAULT_MODEL])
        input_cost = (input_tokens / 1_000_000) * model_info["input_price"]
        output_cost = (output_tokens / 1_000_000) * model_info["output_price"]
        return round(input_cost + output_cost, 6)
