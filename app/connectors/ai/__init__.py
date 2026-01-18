"""AI Provider Connectors"""
from .base import AIProviderBase, AIMessage, AIResponse
from .claude import ClaudeConnector
from .openai import OpenAIConnector
from .jais import JaisConnector
from .router import SmartRouter

# Global router instance
smart_router = SmartRouter()

__all__ = [
    "AIProviderBase",
    "AIMessage",
    "AIResponse",
    "ClaudeConnector",
    "OpenAIConnector",
    "JaisConnector",
    "SmartRouter",
    "smart_router"
]
