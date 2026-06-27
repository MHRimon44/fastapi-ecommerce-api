from app.vectorstores.file_vector_store import FileVectorStore


def test_file_vector_store_add_chunk_persists_data(tmp_path):
    storage_path = tmp_path / "vector_store.json"

    store = FileVectorStore(
        storage_path=str(storage_path),
    )

    store.add_chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Return Policy",
        content="Customers can return products within 7 days.",
        vector={
            "return": 1.0,
            "products": 1.0,
            "days": 1.0,
        },
        source_type="policy",
    )

    new_store = FileVectorStore(
        storage_path=str(storage_path),
    )

    assert new_store.count() == 1


def test_file_vector_store_search_returns_relevant_result(tmp_path):
    storage_path = tmp_path / "vector_store.json"

    store = FileVectorStore(
        storage_path=str(storage_path),
    )

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


def test_file_vector_store_clear_removes_data(tmp_path):
    storage_path = tmp_path / "vector_store.json"

    store = FileVectorStore(
        storage_path=str(storage_path),
    )

    store.add_chunk(
        chunk_id="chunk-1",
        document_id="doc-1",
        title="Delivery Policy",
        content="Delivery takes 3 to 5 business days.",
        vector={
            "delivery": 1.0,
            "days": 1.0,
        },
        source_type="policy",
    )

    assert store.count() == 1

    store.clear()

    assert store.count() == 0
