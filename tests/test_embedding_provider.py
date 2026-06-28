from app.providers.embedding_provider import MockEmbeddingProvider
from app.vectorstores.in_memory_vector_store import InMemoryVectorStore


def test_mock_embedding_provider_returns_sparse_vector():
    provider = MockEmbeddingProvider()

    vector = provider.create_embedding(
        "voucher discount voucher checkout"
    )

    assert vector["voucher"] == 2.0
    assert vector["discount"] == 1.0
    assert vector["checkout"] == 1.0


def test_sparse_cosine_similarity_returns_positive_score():
    store = InMemoryVectorStore()

    vector_a = {
        "voucher": 1.0,
        "discount": 1.0,
    }

    vector_b = {
        "voucher": 1.0,
        "checkout": 1.0,
    }

    score = store._cosine_similarity(
        vector_a,
        vector_b,
    )

    assert score > 0
