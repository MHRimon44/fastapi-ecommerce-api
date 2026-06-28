from app.providers.rag_answer_provider import MockRAGAnswerProvider
from app.schemas.rag_schema import RAGSearchResult


def test_mock_rag_answer_provider_returns_context_based_answer():
    provider = MockRAGAnswerProvider()

    sources = [
        RAGSearchResult(
            chunk_id="chunk-1",
            document_id="doc-1",
            title="Voucher Policy",
            content="Voucher discount can be applied during checkout.",
            score=0.95,
        )
    ]

    answer = provider.generate_answer(
        question="How can voucher discount be applied?",
        sources=sources,
    )

    assert "retrieved document context" in answer
    assert "Voucher discount" in answer


def test_mock_rag_answer_provider_handles_no_sources():
    provider = MockRAGAnswerProvider()

    answer = provider.generate_answer(
        question="Unknown question",
        sources=[],
    )

    assert "could not find relevant information" in answer
