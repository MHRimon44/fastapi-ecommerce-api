import json
from typing import List

from fastapi import HTTPException, status

from app.core.config import settings
from app.prompts.rag_prompts import build_rag_answer_prompt
from app.schemas.rag_schema import RAGSearchResult


class MockRAGAnswerProvider:
    def generate_answer(
        self,
        question: str,
        sources: List[RAGSearchResult],
    ) -> str:
        if not sources:
            return "I could not find relevant information from the indexed documents."

        best_source = sources[0]

        return (
            "Based on the retrieved document context, "
            f"{best_source.content}"
        )


class OpenAIRAGAnswerProvider:
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

    def generate_answer(
        self,
        question: str,
        sources: List[RAGSearchResult],
    ) -> str:
        prompt = build_rag_answer_prompt(
            question=question,
            sources=sources,
        )

        try:
            response = self.client.responses.create(
                model=settings.AI_MODEL_NAME,
                instructions=(
                    "You are a RAG answer generation assistant. "
                    "Return only valid JSON. Do not include markdown."
                ),
                input=prompt,
            )

            data = json.loads(response.output_text)

            return data["answer"]

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned invalid JSON",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider request failed",
            )


def get_rag_answer_provider():
    if settings.AI_PROVIDER == "mock":
        return MockRAGAnswerProvider()

    if settings.AI_PROVIDER == "openai":
        return OpenAIRAGAnswerProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported AI provider",
    )
