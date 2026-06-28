import pytest

from app.vectorstores.file_vector_store import vector_store


@pytest.fixture(autouse=True)
def clear_vector_store():
    vector_store.clear()
    yield
    vector_store.clear()


def index_inventory_policy(client):
    return client.post(
        "/knowledge/erp-policies/index",
        json={
            "policy_title": "Inventory Stock Adjustment Policy",
            "module_name": "Inventory",
            "department": "Warehouse",
            "policy_content": (
                "Stock adjustment can be created only when physical stock and "
                "system stock do not match. The adjustment must include a valid "
                "reason, approval note, and warehouse reference."
            ),
            "rules": [
                "Stock adjustment requires supervisor approval",
                "Adjustment reason is mandatory",
                "Warehouse reference must be provided",
            ],
            "tags": [
                "inventory",
                "stock",
                "warehouse",
                "approval",
            ],
        },
    )


def test_index_erp_policy_success(client):
    response = index_inventory_policy(client)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "ERP policy indexed successfully"
    assert body["data"]["document_id"]
    assert body["data"]["policy_title"] == "Inventory Stock Adjustment Policy"
    assert body["data"]["chunks_count"] >= 1


def test_index_erp_policy_validation_error(client):
    response = client.post(
        "/knowledge/erp-policies/index",
        json={
            "policy_title": "A",
            "policy_content": "short",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_search_erp_policy_success(client):
    index_inventory_policy(client)

    response = client.post(
        "/knowledge/erp-policies/search",
        json={
            "query": "stock adjustment warehouse approval",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "ERP policy search completed successfully"
    assert len(body["data"]) >= 1
    assert body["data"][0]["title"] == "Inventory Stock Adjustment Policy"
    assert body["data"][0]["score"] > 0


def test_ask_erp_policy_success(client):
    index_inventory_policy(client)

    response = client.post(
        "/knowledge/erp-policies/ask",
        json={
            "question": "When can stock adjustment be created?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "ERP policy answer generated successfully"
    assert "Inventory Stock Adjustment Policy" in body["data"]["answer"]
    assert len(body["data"]["sources"]) >= 1


def test_erp_policy_does_not_return_product_source(client):
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
        "/knowledge/erp-policies/search",
        json={
            "query": "office laptop backpack",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"] == []
