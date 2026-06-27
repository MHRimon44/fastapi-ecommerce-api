import pytest

from app.vectorstores.file_vector_store import vector_store


@pytest.fixture(autouse=True)
def clear_vector_store():
    vector_store.clear()
    yield
    vector_store.clear()


def index_laptop_backpack(client):
    return client.post(
        "/knowledge/products/index",
        json={
            "product_name": "Laptop Backpack",
            "sku": "BAG-LAP-001",
            "category": "Backpack",
            "description": (
                "A professional laptop backpack designed for office users, "
                "daily commuting, and carrying a 15 inch laptop safely."
            ),
            "features": [
                "15 inch laptop compartment",
                "water resistant fabric",
                "lightweight design",
            ],
            "price": 1599,
            "stock_qty": 120,
            "use_case": "Office laptop carry and daily commute",
        },
    )


def test_index_product_knowledge_success(client):
    response = index_laptop_backpack(client)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Product knowledge indexed successfully"
    assert body["data"]["document_id"]
    assert body["data"]["product_name"] == "Laptop Backpack"
    assert body["data"]["chunks_count"] >= 1


def test_index_product_knowledge_validation_error(client):
    response = client.post(
        "/knowledge/products/index",
        json={
            "product_name": "A",
            "description": "short",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_search_product_knowledge_success(client):
    index_laptop_backpack(client)

    response = client.post(
        "/knowledge/products/search",
        json={
            "query": "office laptop backpack",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Product knowledge search completed successfully"
    assert len(body["data"]) >= 1
    assert body["data"][0]["title"] == "Laptop Backpack"
    assert body["data"][0]["score"] > 0


def test_ask_product_knowledge_success(client):
    index_laptop_backpack(client)

    response = client.post(
        "/knowledge/products/ask",
        json={
            "question": "Which backpack is good for office laptop use?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Product knowledge answer generated successfully"
    assert "Laptop Backpack" in body["data"]["answer"]
    assert len(body["data"]["sources"]) >= 1


def test_product_knowledge_does_not_return_policy_source(client):
    client.post(
        "/rag/documents/index",
        json={
            "title": "Return Policy",
            "content": (
                "Customers can return products within 7 days after delivery. "
                "Refunds are processed after quality check."
            ),
            "source_type": "policy",
        },
    )

    response = client.post(
        "/knowledge/products/search",
        json={
            "query": "return products refund",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"] == []
