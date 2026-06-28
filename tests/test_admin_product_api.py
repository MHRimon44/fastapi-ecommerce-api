import pytest

from app.main import app
from app.dependencies.auth_guard import require_authenticated_user, require_admin_user


@pytest.fixture(autouse=True)
def use_real_auth_guard_for_admin_product_tests(client):
    """
    Some shared test fixtures may override auth dependencies.
    Admin product tests must use real JWT auth because they verify:
    - no token returns 401
    - customer role returns 403
    - admin role can access product APIs
    """
    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)

    yield

    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)


from app.core.security import create_access_token


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


def test_admin_create_product_success(client):
    response = client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Office Laptop Backpack",
            "sku": "BAG-ADMIN-001",
            "price": 1250,
            "stock_qty": 15,
            "description": "Professional backpack for office use",
            "is_active": True,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Product created successfully"
    assert body["data"]["product_name"] == "Office Laptop Backpack"
    assert body["data"]["sku"] == "BAG-ADMIN-001"
    assert body["data"]["price"] == 1250
    assert body["data"]["stock_qty"] == 15
    assert body["data"]["is_active"] is True


def test_admin_list_products_success(client):
    client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Travel Backpack",
            "sku": "BAG-ADMIN-002",
            "price": 1550,
            "stock_qty": 8,
            "description": "Travel backpack",
            "is_active": True,
        },
    )

    response = client.get(
        "/admin/products",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Products retrieved successfully"
    assert body["total"] >= 1
    assert len(body["data"]) >= 1


def test_admin_get_product_success(client):
    create_response = client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Laptop Bag",
            "sku": "BAG-ADMIN-003",
            "price": 1000,
            "stock_qty": 5,
            "description": "Laptop bag",
            "is_active": True,
        },
    )

    product_id = create_response.json()["data"]["product_id"]

    response = client.get(
        f"/admin/products/{product_id}",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["data"]["product_id"] == product_id


def test_admin_update_product_success(client):
    create_response = client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Old Product Name",
            "sku": "BAG-ADMIN-004",
            "price": 900,
            "stock_qty": 4,
            "description": "Old description",
            "is_active": True,
        },
    )

    product_id = create_response.json()["data"]["product_id"]

    response = client.put(
        f"/admin/products/{product_id}",
        headers=get_admin_headers(),
        json={
            "product_name": "Updated Product Name",
            "price": 1100,
            "description": "Updated description",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Product updated successfully"
    assert body["data"]["product_name"] == "Updated Product Name"
    assert body["data"]["price"] == 1100


def test_admin_update_product_stock_success(client):
    create_response = client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Stock Product",
            "sku": "BAG-ADMIN-005",
            "price": 800,
            "stock_qty": 3,
            "description": "Stock test",
            "is_active": True,
        },
    )

    product_id = create_response.json()["data"]["product_id"]

    response = client.patch(
        f"/admin/products/{product_id}/stock",
        headers=get_admin_headers(),
        json={
            "stock_qty": 25,
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["stock_qty"] == 25


def test_admin_update_product_status_success(client):
    create_response = client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Status Product",
            "sku": "BAG-ADMIN-006",
            "price": 850,
            "stock_qty": 7,
            "description": "Status test",
            "is_active": True,
        },
    )

    product_id = create_response.json()["data"]["product_id"]

    response = client.patch(
        f"/admin/products/{product_id}/status",
        headers=get_admin_headers(),
        json={
            "is_active": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["data"]["is_active"] is False


def test_admin_delete_product_success(client):
    create_response = client.post(
        "/admin/products",
        headers=get_admin_headers(),
        json={
            "product_name": "Delete Product",
            "sku": "BAG-ADMIN-007",
            "price": 700,
            "stock_qty": 2,
            "description": "Delete test",
            "is_active": True,
        },
    )

    product_id = create_response.json()["data"]["product_id"]

    response = client.delete(
        f"/admin/products/{product_id}",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"

    get_response = client.get(
        f"/admin/products/{product_id}",
        headers=get_admin_headers(),
    )

    assert get_response.status_code == 404


def test_admin_product_without_token_error(client):
    response = client.get("/admin/products")

    assert response.status_code == 401


def test_admin_product_customer_role_forbidden(client):
    token = create_access_token(
        subject="2",
        extra_payload={
            "user_id": 2,
            "email": "customer@example.com",
            "role": "Customer",
        },
    )

    response = client.get(
        "/admin/products",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
