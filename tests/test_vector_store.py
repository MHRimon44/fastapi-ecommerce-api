from app.vectorstores.in_memory_vector_store import InMemoryVectorStore


def test_vector_store_add_chunk_success():
    store = InMemoryVectorStore()

    store.add_chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Voucher Policy",
        content="Voucher discount can be applied during checkout.",
        vector={
            "voucher": 1.0,
            "discount": 1.0,
            "checkout": 1.0,
        },
        source_type="policy",
    )

    assert store.count() == 1


def test_vector_store_search_returns_relevant_chunk():
    store = InMemoryVectorStore()

    store.add_chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Voucher Policy",
        content="Voucher discount can be applied during checkout.",
        vector={
            "voucher": 1.0,
            "discount": 1.0,
            "checkout": 1.0,
        },
        source_type="policy",
    )

    results = store.search(
        query_vector={
            "voucher": 1.0,
            "checkout": 1.0,
        },
        top_k=3,
    )

    assert len(results) == 1
    assert results[0].title == "Voucher Policy"
    assert results[0].score > 0


def test_vector_store_search_returns_empty_when_no_match():
    store = InMemoryVectorStore()

    store.add_chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Voucher Policy",
        content="Voucher discount can be applied during checkout.",
        vector={
            "voucher": 1.0,
            "discount": 1.0,
        },
        source_type="policy",
    )

    results = store.search(
        query_vector={
            "volcano": 1.0,
            "astronomy": 1.0,
        },
        top_k=3,
    )

    assert results == []
