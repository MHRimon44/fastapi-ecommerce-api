import re
from collections import Counter
from typing import Dict, List, Union

from fastapi import HTTPException, status

from app.core.config import settings


EmbeddingVector = Union[Dict[str, float], List[float]]


class MockEmbeddingProvider:
    def create_embedding(
        self,
        text: str,
    ) -> EmbeddingVector:
        tokens = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower(),
        )

        token_counts = Counter(tokens)

        return {
            token: float(count)
            for token, count in token_counts.items()
        }


class OpenAIEmbeddingProvider:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured",
            )

        from openai import OpenAI

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=30.0,
        )

    def create_embedding(
        self,
        text: str,
    ) -> EmbeddingVector:
        try:
            response = self.client.embeddings.create(
                model=settings.EMBEDDING_MODEL_NAME,
                input=text,
            )

            return response.data[0].embedding

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Embedding provider request failed",
            )


def get_embedding_provider():
    if settings.EMBEDDING_PROVIDER == "mock":
        return MockEmbeddingProvider()

    if settings.EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddingProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported embedding provider",
    )
