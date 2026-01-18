"""Smart Router for AI Provider Selection"""
from typing import List, Optional, Tuple
from .base import AIProviderBase, AIMessage, AIResponse
from .claude import ClaudeConnector
from .openai import OpenAIConnector
from .jais import JaisConnector
import re


class SmartRouter:
    """
    Intelligent router that selects the best AI provider based on:
    - Query language (Arabic -> Jais preference)
    - Query complexity
    - Cost optimization
    - User preferences
    """

    def __init__(self):
        self.providers = {
            "claude": ClaudeConnector(),
            "openai": OpenAIConnector(),
            "jais": JaisConnector()
        }

        # Routing rules
        self.ROUTING_RULES = {
            "arabic_simple": ["jais", "claude", "openai"],      # Arabic, simple query
            "arabic_complex": ["claude", "jais", "openai"],     # Arabic, complex query
            "english_simple": ["claude", "openai"],             # English, simple
            "english_complex": ["claude", "openai"],            # English, complex
            "cost_optimized": ["jais", "openai", "claude"],     # Cheapest first
            "quality_first": ["claude", "openai", "jais"]       # Best quality first
        }

    def detect_language(self, text: str) -> str:
        """Detect if text is primarily Arabic or English"""
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
        arabic_chars = len(arabic_pattern.findall(text))
        total_chars = len(text.replace(" ", ""))

        if total_chars == 0:
            return "en"

        arabic_ratio = arabic_chars / total_chars
        return "ar" if arabic_ratio > 0.3 else "en"

    def estimate_complexity(self, messages: List[AIMessage]) -> str:
        """Estimate query complexity: simple, medium, complex"""
        total_length = sum(len(msg.content) for msg in messages)

        # Check for complexity indicators
        complex_indicators = [
            "تحليل", "تفصيل", "شرح", "مقارنة", "استراتيجية",
            "analyze", "detailed", "explain", "compare", "strategy",
            "code", "برمجة", "كود"
        ]

        last_message = messages[-1].content.lower() if messages else ""
        has_complex_words = any(word in last_message for word in complex_indicators)

        if total_length > 2000 or has_complex_words:
            return "complex"
        elif total_length > 500:
            return "medium"
        else:
            return "simple"

    def select_provider(
        self,
        messages: List[AIMessage],
        preferred_provider: Optional[str] = None,
        routing_strategy: str = "auto"
    ) -> Tuple[str, str, AIProviderBase]:
        """
        Select the best provider for the request

        Returns: (provider_id, model_id, provider_instance)
        """

        # If user specified a provider, use it
        if preferred_provider and preferred_provider in self.providers:
            provider = self.providers[preferred_provider]
            return preferred_provider, provider.DEFAULT_MODEL, provider

        # Auto-routing logic
        last_message = messages[-1].content if messages else ""
        language = self.detect_language(last_message)
        complexity = self.estimate_complexity(messages)

        # Determine routing key
        if routing_strategy == "cost":
            routing_key = "cost_optimized"
        elif routing_strategy == "quality":
            routing_key = "quality_first"
        else:
            # Auto: based on language and complexity
            lang_prefix = "arabic" if language == "ar" else "english"
            routing_key = f"{lang_prefix}_{complexity}"
            if routing_key not in self.ROUTING_RULES:
                routing_key = "english_simple"

        # Get provider order
        provider_order = self.ROUTING_RULES.get(routing_key, ["claude"])

        # Select first available provider
        for provider_id in provider_order:
            provider = self.providers.get(provider_id)
            if provider:
                # Select appropriate model based on complexity
                model = self._select_model(provider, complexity)
                return provider_id, model, provider

        # Fallback to Claude
        provider = self.providers["claude"]
        return "claude", provider.DEFAULT_MODEL, provider

    def _select_model(self, provider: AIProviderBase, complexity: str) -> str:
        """Select appropriate model tier based on complexity"""
        models = provider.get_available_models()

        tier_map = {
            "simple": "fast",
            "medium": "balanced",
            "complex": "powerful"
        }

        target_tier = tier_map.get(complexity, "balanced")

        # Find model matching tier
        for model in models:
            if model.get("tier") == target_tier:
                return model["id"]

        # Fallback to default
        return provider.DEFAULT_MODEL

    async def route_and_execute(
        self,
        messages: List[AIMessage],
        preferred_provider: Optional[str] = None,
        preferred_model: Optional[str] = None,
        routing_strategy: str = "auto",
        **kwargs
    ) -> Tuple[AIResponse, dict]:
        """
        Route request to best provider and execute

        Returns: (response, routing_info)
        """

        provider_id, model_id, provider = self.select_provider(
            messages, preferred_provider, routing_strategy
        )

        # Use preferred model if specified
        if preferred_model:
            model_id = preferred_model

        # Execute request
        response = await provider.chat(
            messages=messages,
            model=model_id,
            **kwargs
        )

        # Calculate cost
        cost = provider.calculate_cost(
            response.input_tokens,
            response.output_tokens,
            model_id
        )

        routing_info = {
            "selected_provider": provider_id,
            "selected_model": model_id,
            "language_detected": self.detect_language(messages[-1].content if messages else ""),
            "complexity": self.estimate_complexity(messages),
            "routing_strategy": routing_strategy,
            "cost_usd": cost
        }

        return response, routing_info

    def get_all_providers_status(self) -> List[dict]:
        """Get status of all providers"""
        result = []
        for provider_id, provider in self.providers.items():
            is_configured = bool(provider.api_key if hasattr(provider, 'api_key') else False)
            result.append({
                "id": provider_id,
                "name": provider.provider_name,
                "name_ar": provider.provider_name_ar,
                "status": "active" if is_configured else "not_configured",
                "models": provider.get_available_models()
            })
        return result
