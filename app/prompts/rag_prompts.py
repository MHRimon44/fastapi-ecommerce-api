from typing import List

from app.schemas.rag_schema import RAGSearchResult


def build_rag_answer_prompt(
    question: str,
    sources: List[RAGSearchResult],
) -> str:
    context_parts = []

    for index, source in enumerate(sources, start=1):
        context_parts.append(
            f"Source {index}: {source.content}"
        )

    context = "\n\n".join(context_parts)

    return f"""
You are a helpful business knowledge assistant.

Answer the question using only the provided context.

Rules:
- Do not make up information.
- If the answer is not in the context, say that the information is not available.
- Keep the answer clear and concise.
- Return only valid JSON.
- Do not include markdown.

Question:
{question}

Context:
{context}

Return JSON only in this exact format:
{{
  "answer": "final answer here"
}}
"""
