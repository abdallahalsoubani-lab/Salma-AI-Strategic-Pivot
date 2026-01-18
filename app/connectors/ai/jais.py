"""Jais (G42) API Connector - Arabic-First LLM"""
import httpx
import json
from typing import List, Optional, AsyncIterator
from app.config import settings
from .base import AIProviderBase, AIMessage, AIResponse


class JaisConnector(AIProviderBase):
    """
    Jais (G42) API Connector
    Arabic-first large language model
    """

    provider_id = "jais"
    provider_name = "Jais (G42)"
    provider_name_ar = "جيس (جي42)"

    # Note: Update this URL based on actual Jais API endpoint
    API_URL = "https://api.g42.ai/v1/chat/completions"  # Placeholder

    MODELS = {
        "jais-30b-chat": {
            "name": "Jais 30B Chat",
            "name_ar": "جيس 30 مليار محادثة",
            "input_price": 0.0,   # Currently free tier available
            "output_price": 0.0,
            "max_tokens": 2048,
            "context_window": 8192,
            "tier": "arabic",
            "languages": ["ar", "en"]
        },
        "jais-13b-chat": {
            "name": "Jais 13B Chat",
            "name_ar": "جيس 13 مليار محادثة",
            "input_price": 0.0,
            "output_price": 0.0,
            "max_tokens": 2048,
            "context_window": 8192,
            "tier": "arabic-fast",
            "languages": ["ar", "en"]
        }
    }

    DEFAULT_MODEL = "jais-30b-chat"

    def __init__(self):
        self.api_key = settings.JAIS_API_KEY
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=120.0
        )
        self.is_available = bool(self.api_key)

    async def chat(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Send chat request to Jais API"""

        if not self.is_available:
            raise Exception("Jais API key not configured")

        model = model or self.DEFAULT_MODEL

        # Add Arabic system prompt for better Arabic responses
        default_system = "أنت مساعد ذكي يتحدث العربية بطلاقة. أجب دائماً باللغة التي يستخدمها المستخدم."
        system = system_prompt or default_system

        api_messages = [{"role": "system", "content": system}]

        for msg in messages:
            if msg.role != "system":
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
            model=model,
            provider=self.provider_id,
            input_tokens=data.get("usage", {}).get("prompt_tokens", 0),
            output_tokens=data.get("usage", {}).get("completion_tokens", 0),
            finish_reason=data["choices"][0].get("finish_reason", "stop")
        )

    async def chat_stream(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream chat response from Jais API"""

        if not self.is_available:
            raise Exception("Jais API key not configured")

        model = model or self.DEFAULT_MODEL

        default_system = "أنت مساعد ذكي يتحدث العربية بطلاقة. أجب دائماً باللغة التي يستخدمها المستخدم."
        system = system_prompt or default_system

        api_messages = [{"role": "system", "content": system}]

        for msg in messages:
            if msg.role != "system":
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

        # Jais follows OpenAI-compatible API format
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
        """Return list of available models"""
        return [
            {
                "id": model_id,
                "name": info["name"],
                "name_ar": info["name_ar"],
                "tier": info["tier"],
                "input_price": info["input_price"],
                "output_price": info["output_price"],
                "context_window": info["context_window"],
                "languages": info["languages"]
            }
            for model_id, info in self.MODELS.items()
        ]

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        # Arabic text typically has fewer tokens per character
        return len(text) // 2

    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost in USD"""
        # Currently free tier
        return 0.0
