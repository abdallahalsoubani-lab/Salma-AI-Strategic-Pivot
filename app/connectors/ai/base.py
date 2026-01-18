"""Base class for all AI provider connectors"""
from abc import ABC, abstractmethod
from typing import List, Optional, AsyncIterator
from pydantic import BaseModel


class AIMessage(BaseModel):
    """Message in AI conversation"""
    role: str  # user, assistant, system
    content: str


class AIResponse(BaseModel):
    """Response from AI provider"""
    content: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    finish_reason: str


class AIProviderBase(ABC):
    """Base class for all AI provider connectors"""

    provider_id: str
    provider_name: str
    provider_name_ar: str
    DEFAULT_MODEL: str

    @abstractmethod
    async def chat(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> AIResponse:
        """Send chat request to AI provider"""
        pass

    @abstractmethod
    async def chat_stream(
        self,
        messages: List[AIMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ) -> AsyncIterator[str]:
        """Stream chat response from AI provider"""
        pass

    @abstractmethod
    def get_available_models(self) -> List[dict]:
        """Return list of available models with pricing"""
        pass

    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost in USD"""
        pass
