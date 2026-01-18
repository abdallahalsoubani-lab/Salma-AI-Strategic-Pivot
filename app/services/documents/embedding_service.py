"""
خدمة التضمين (Embeddings)
Embedding Service for Vector Search
"""

from typing import List, Optional
import httpx
import numpy as np
from dataclasses import dataclass

from app.config import settings


@dataclass
class EmbeddingResult:
    """نتيجة التضمين"""
    text: str
    embedding: List[float]
    model: str
    token_count: int


class EmbeddingService:
    """خدمة إنشاء الـ Embeddings"""

    # Model configurations
    MODELS = {
        "openai": {
            "name": "text-embedding-3-small",
            "dimensions": 1536,
            "max_tokens": 8191,
            "cost_per_1m": 0.02
        },
        "openai-large": {
            "name": "text-embedding-3-large",
            "dimensions": 3072,
            "max_tokens": 8191,
            "cost_per_1m": 0.13
        },
        "cohere": {
            "name": "embed-multilingual-v3.0",
            "dimensions": 1024,
            "max_tokens": 512,
            "cost_per_1m": 0.10
        }
    }

    DEFAULT_MODEL = "openai"

    def __init__(self, model: str = None):
        self.model = model or self.DEFAULT_MODEL
        self.model_config = self.MODELS[self.model]

        # Initialize HTTP client
        self.client = httpx.AsyncClient(timeout=60.0)

    async def embed_text(self, text: str) -> EmbeddingResult:
        """إنشاء embedding لنص واحد"""

        embeddings = await self.embed_texts([text])
        return embeddings[0]

    async def embed_texts(self, texts: List[str]) -> List[EmbeddingResult]:
        """إنشاء embeddings لعدة نصوص"""

        if self.model.startswith("openai"):
            return await self._embed_openai(texts)
        elif self.model == "cohere":
            return await self._embed_cohere(texts)
        else:
            raise ValueError(f"Unsupported embedding model: {self.model}")

    async def _embed_openai(self, texts: List[str]) -> List[EmbeddingResult]:
        """OpenAI Embeddings API"""

        response = await self.client.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model_config["name"],
                "input": texts
            }
        )

        response.raise_for_status()
        data = response.json()

        results = []
        for i, item in enumerate(data["data"]):
            results.append(EmbeddingResult(
                text=texts[i],
                embedding=item["embedding"],
                model=self.model_config["name"],
                token_count=data["usage"]["total_tokens"] // len(texts)
            ))

        return results

    async def _embed_cohere(self, texts: List[str]) -> List[EmbeddingResult]:
        """Cohere Embeddings API (better for Arabic)"""

        response = await self.client.post(
            "https://api.cohere.ai/v1/embed",
            headers={
                "Authorization": f"Bearer {settings.COHERE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model_config["name"],
                "texts": texts,
                "input_type": "search_document"
            }
        )

        response.raise_for_status()
        data = response.json()

        results = []
        for i, embedding in enumerate(data["embeddings"]):
            results.append(EmbeddingResult(
                text=texts[i],
                embedding=embedding,
                model=self.model_config["name"],
                token_count=len(texts[i]) // 4
            ))

        return results

    def calculate_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """حساب التشابه بين embedding"""

        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        return float(similarity)
