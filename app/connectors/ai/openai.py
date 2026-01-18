"""OpenAI GPT API Connector"""
import httpx
import json
from typing import List, Optional, AsyncIterator
from app.config import settings
from .base import AIProviderBase, AIMessage, AIResponse


class OpenAIConnector(AIProviderBase):
    """OpenAI GPT API Connector"""

    provider_id = "openai"
    provider_name = "OpenAI"
    provider_name_ar = "أوبن إيه آي"

    API_URL = "https://api.openai.com/v1/chat/completions"

    MODELS = {
        "gpt-4o": {
            "name": "GPT-4o",
            "name_ar": "جي بي تي-4 أو",
            "input_price": 2.50,
            "output_price": 10.0,
            "max_tokens": 4096,
            "context_window": 128000,
            "tier": "balanced"
        },
        "gpt-4o-mini": {
            "name": "GPT-4o Mini",
            "name_ar": "جي بي تي-4 أو ميني",
            "input_price": 0.15,
            "output_price": 0.60,
            "max_tokens": 4096,
            "context_window": 128000,
            "tier": "fast"
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "name_ar": "جي بي تي-4 تيربو",
            "input_price": 10.0,
            "output_price": 30.0,
            "max_tokens": 4096,
            "context_window": 128000,
            "tier": "powerful"
        }
    }

    DEFAULT_MODEL = "gpt-4o"

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
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
        """Send chat request to OpenAI API"""

        model = model or self.DEFAULT_MODEL

        api_messages = []

        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})

        for msg in messages:
            api_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        payload = {
            "model": model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = await self.client.post(self.API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        return AIResponse(
            content=data["choices"][0]["message"]["content"],
            model=data["model"],
            provider=self.provider_id,
            input_tokens=data["usage"]["prompt_tokens"],
            output_tokens=data["usage"]["completion_tokens"],
            finish_reason=data["choices"][0]["finish_reason"]
        )

    async def chat_stream(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream chat response from OpenAI API"""

        model = model or self.DEFAULT_MODEL

        api_messages = []

        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})

        for msg in messages:
            api_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        payload = {
            "model": model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }

        async with self.client.stream("POST", self.API_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        data = json.loads(line[6:])
                        if data["choices"][0]["delta"].get("content"):
                            yield data["choices"][0]["delta"]["content"]
                    except (json.JSONDecodeError, KeyError, IndexError):
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
        return len(text) // 4

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost in USD"""
        model_info = self.MODELS.get(model, self.MODELS[self.DEFAULT_MODEL])
        input_cost = (input_tokens / 1_000_000) * model_info["input_price"]
        output_cost = (output_tokens / 1_000_000) * model_info["output_price"]
        return round(input_cost + output_cost, 6)
