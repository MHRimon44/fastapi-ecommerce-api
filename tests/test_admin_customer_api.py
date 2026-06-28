import pytest

from app.main import app
from app.core.security import create_access_token
from app.dependencies.auth_guard import require_authenticated_user, require_admin_user


@pytest.fixture(autouse=True)
def use_real_auth_guard_for_admin_customer_tests(client):
    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)

    yield

    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)


def get_admin_headers():
    token = create_access_token(
        subject="1",
        extra_payload={
            "user_id": 1,
            "email": "admin@example.com",
            "role": "Admin",
        },
    )

    return {
        "Authorization": f"Bearer {token}",
    }


def test_admin_create_customer_success(client):
    response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Rahim Uddin",
            "phone": "01711111111",
            "email": "rahim@example.com",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Customer created successfully"
    assert body["data"]["customer_name"] == "Rahim Uddin"
    assert body["data"]["phone"] == "01711111111"
    assert body["data"]["email"] == "rahim@example.com"


def test_admin_create_customer_invalid_phone_error(client):
    response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Invalid Phone",
            "phone": "12345",
            "email": "invalid@example.com",
        },
    )

    assert response.status_code == 422


def test_admin_create_customer_duplicate_phone_error(client):
    payload = {
        "customer_name": "Duplicate Phone",
        "phone": "01722222222",
        "email": "duplicate1@example.com",
    }

    first_response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Duplicate Phone 2",
            "phone": "01722222222",
            "email": "duplicate2@example.com",
        },
    )

    assert second_response.status_code == 400

    body = second_response.json()

    assert (
        body.get("detail") == "Customer phone already exists"
        or body.get("message") == "Customer phone already exists"
    )


def test_admin_list_customers_success(client):
    client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "List Customer",
            "phone": "01733333333",
            "email": "list@example.com",
        },
    )

    response = client.get(
        "/admin/customers",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Customers retrieved successfully"
    assert body["total"] >= 1
    assert len(body["data"]) >= 1


def test_admin_search_customers_success(client):
    client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Searchable Customer",
            "phone": "01744444444",
            "email": "searchable@example.com",
        },
    )

    response = client.get(
        "/admin/customers?search=Searchable",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_admin_get_customer_success(client):
    create_response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Single Customer",
            "phone": "01755555555",
            "email": "single@example.com",
        },
    )

    customer_id = create_response.json()["data"]["customer_id"]

    response = client.get(
        f"/admin/customers/{customer_id}",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["data"]["customer_id"] == customer_id


def test_admin_update_customer_success(client):
    create_response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Old Customer",
            "phone": "01766666666",
            "email": "old@example.com",
        },
    )

    customer_id = create_response.json()["data"]["customer_id"]

    response = client.put(
        f"/admin/customers/{customer_id}",
        headers=get_admin_headers(),
        json={
            "customer_name": "Updated Customer",
            "phone": "01777777777",
            "email": "updated@example.com",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Customer updated successfully"
    assert body["data"]["customer_name"] == "Updated Customer"
    assert body["data"]["phone"] == "01777777777"


def test_admin_delete_customer_success(client):
    create_response = client.post(
        "/admin/customers",
        headers=get_admin_headers(),
        json={
            "customer_name": "Delete Customer",
            "phone": "01788888888",
            "email": "delete@example.com",
        },
    )

    customer_id = create_response.json()["data"]["customer_id"]

    response = client.delete(
        f"/admin/customers/{customer_id}",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Customer deleted successfully"

    get_response = client.get(
        f"/admin/customers/{customer_id}",
        headers=get_admin_headers(),
    )

    assert get_response.status_code == 404


def test_admin_customer_without_token_error(client):
    response = client.get("/admin/customers")

    assert response.status_code == 401


def test_admin_customer_customer_role_forbidden(client):
    token = create_access_token(
        subject="2",
        extra_payload={
            "user_id": 2,
            "email": "customer@example.com",
            "role": "Customer",
        },
    )

    response = client.get(
        "/admin/customers",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
