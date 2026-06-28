from app.prompts.rag_prompts import build_rag_answer_prompt
from app.schemas.rag_schema import RAGSearchResult


def test_build_rag_answer_prompt_contains_question_and_context():
    sources = [
        RAGSearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            title="Return Policy",
            content="Customers can return products within 7 days.",
            score=0.9,
        )
    ]

    prompt = build_rag_answer_prompt(
        question="What is the return policy?",
        sources=sources,
    )

    assert "What is the return policy?" in prompt
    assert "Customers can return products within 7 days." in prompt
    assert '"answer"' in prompt
