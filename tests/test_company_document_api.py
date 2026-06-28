import pytest

from app.vectorstores.file_vector_store import vector_store


@pytest.fixture(autouse=True)
def clear_vector_store():
    vector_store.clear()
    yield
    vector_store.clear()


def index_leave_policy(client):
    return client.post(
        "/knowledge/company-documents/index",
        json={
            "document_title": "Employee Leave Policy",
            "department": "HR",
            "document_type": "Policy",
            "content": (
                "Employees can apply for annual leave after approval from their "
                "department manager. Emergency leave should be reported to HR as "
                "soon as possible. Leave balance must be checked before applying."
            ),
            "tags": [
                "leave",
                "hr",
                "employee",
            ],
        },
    )


def test_index_company_document_success(client):
    response = index_leave_policy(client)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Company document indexed successfully"
    assert body["data"]["document_id"]
    assert body["data"]["document_title"] == "Employee Leave Policy"
    assert body["data"]["chunks_count"] >= 1


def test_index_company_document_validation_error(client):
    response = client.post(
        "/knowledge/company-documents/index",
        json={
            "document_title": "A",
            "content": "short",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_search_company_document_success(client):
    index_leave_policy(client)

    response = client.post(
        "/knowledge/company-documents/search",
        json={
            "query": "annual leave manager approval HR",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Company document search completed successfully"
    assert len(body["data"]) >= 1
    assert body["data"][0]["title"] == "Employee Leave Policy"
    assert body["data"][0]["score"] > 0


def test_ask_company_document_success(client):
    index_leave_policy(client)

    response = client.post(
        "/knowledge/company-documents/ask",
        json={
            "question": "How can an employee apply for annual leave?",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Company document answer generated successfully"
    assert "Employee Leave Policy" in body["data"]["answer"]
    assert len(body["data"]["sources"]) >= 1


def test_company_document_does_not_return_erp_policy_source(client):
    client.post(
        "/knowledge/erp-policies/index",
        json={
            "policy_title": "Inventory Stock Adjustment Policy",
            "module_name": "Inventory",
            "department": "Warehouse",
            "policy_content": (
                "Stock adjustment can be created only when physical stock and "
                "system stock do not match."
            ),
            "rules": [
                "Stock adjustment requires supervisor approval",
            ],
            "tags": [
                "inventory",
                "stock",
            ],
        },
    )

    response = client.post(
        "/knowledge/company-documents/search",
        json={
            "query": "stock adjustment warehouse approval",
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"] == []
