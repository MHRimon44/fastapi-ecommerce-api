import pytest

from app.vectorstores.file_vector_store import vector_store


@pytest.fixture(autouse=True)
def clear_vector_store():
    vector_store.clear()
    yield
    vector_store.clear()


def index_delivery_delay_guide(client):
    return client.post(
        "/knowledge/support/index",
        json={
            "title": "Delivery Delay Support Guide",
            "issue_type": "delivery_delay",
            "content": (
                "If a customer asks about delayed delivery, first check the courier "
                "tracking status and order dispatch date. If the parcel is already "
                "dispatched, share the tracking update with the customer."
            ),
            "resolution_steps": [
                "Check order dispatch date",
                "Check courier tracking status",
                "Inform customer with clear delivery update",
            ],
            "tags": [
                "delivery",
                "courier",
                "tracking",
            ],
        },
    )


def test_index_support_knowledge_success(client):
    response = index_delivery_delay_guide(client)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Support knowledge indexed successfully"
    assert body["data"]["document_id"]
    assert body["data"]["title"] == "Delivery Delay Support Guide"
    assert body["data"]["chunks_count"] >= 1


def test_index_support_knowledge_validation_error(client):
    response = client.post(
        "/knowledge/support/index",
        json={
            "title": "A",
            "content": "short",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_search_support_knowledge_success(client):
    index_delivery_delay_guide(client)

    response = client.post(
        "/knowledge/support/search",
        json={
            "query": "customer delayed delivery courier tracking",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Support knowledge search completed successfully"
    assert len(body["data"]) >= 1
    assert body["data"][0]["title"] == "Delivery Delay Support Guide"
    assert body["data"][0]["score"] > 0


def test_ask_support_knowledge_success(client):
    index_delivery_delay_guide(client)

    response = client.post(
        "/knowledge/support/ask",
        json={
            "question": "What should support do if delivery is delayed?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Support knowledge answer generated successfully"
    assert "Delivery Delay Support Guide" in body["data"]["answer"]
    assert len(body["data"]["sources"]) >= 1


def test_support_knowledge_does_not_return_product_source(client):
    client.post(
        "/knowledge/products/index",
        json={
            "product_name": "Laptop Backpack",
            "sku": "BAG-LAP-001",
            "category": "Backpack",
            "description": (
                "A professional laptop backpack designed for office users and "
                "daily commuting with a laptop compartment."
            ),
            "features": [
                "laptop compartment",
                "water resistant",
            ],
        },
    )

    response = client.post(
        "/knowledge/support/search",
        json={
            "query": "office laptop backpack",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"] == []
