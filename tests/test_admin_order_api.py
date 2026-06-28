import pytest
from contextlib import contextmanager
from sqlmodel import Session

from app.main import app
from app.core.security import create_access_token
from app.db.session import engine, get_session
from app.dependencies.auth_guard import require_authenticated_user, require_admin_user
from app.models.customer_model import Customer
from app.models.order_model import Order, OrderItem
from app.models.product_model import Product


@pytest.fixture(autouse=True)
def use_real_auth_guard_for_admin_order_tests(client):
    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)

    yield

    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)



@contextmanager
def get_same_test_session_as_api():
    """
    Use the same DB session dependency that FastAPI test client uses.
    This prevents seed data from going to a different database.
    """
    override = app.dependency_overrides.get(get_session)

    if override is None:
        with get_same_test_session_as_api() as session:
            yield session
        return

    dependency_result = override()

    if hasattr(dependency_result, "__next__"):
        session = next(dependency_result)
        try:
            yield session
        finally:
            try:
                next(dependency_result)
            except StopIteration:
                pass
    else:
        yield dependency_result



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


def seed_order(
    order_no="ORD-ADMIN-001",
    order_status="Pending",
):
    with get_same_test_session_as_api() as session:
        customer = Customer(
            customer_name="Admin Order Customer",
            phone="01711111111",
            email="admin.order.customer@example.com",
        )

        session.add(customer)
        session.commit()
        session.refresh(customer)

        product = Product(
            product_name="Admin Order Backpack",
            sku=f"ORDER-BAG-{order_no}",
            price=1000,
            stock_qty=20,
            description="Backpack for admin order test",
            is_active=True,
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        order = Order(
            order_no=order_no,
            customer_id=customer.customer_id,
            order_status=order_status,
            sub_total=1000,
            discount_amount=0,
            total_amount=1000,
            voucher_code=None,
        )

        session.add(order)
        session.commit()
        session.refresh(order)

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=product.product_id,
            quantity=1,
            unit_price=1000,
            line_total=1000,
        )

        session.add(order_item)
        session.commit()
        session.refresh(order_item)

        return {
            "customer_id": customer.customer_id,
            "product_id": product.product_id,
            "order_id": order.order_id,
            "order_item_id": order_item.order_item_id,
            "order_no": order.order_no,
        }


def test_admin_list_orders_success(client):
    seed_order(order_no="ORD-LIST-001")

    response = client.get(
        "/admin/orders",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Orders retrieved successfully"
    assert body["total"] >= 1
    assert len(body["data"]) >= 1


def test_admin_search_orders_success(client):
    seed_order(order_no="ORD-SEARCH-001")

    response = client.get(
        "/admin/orders?search=SEARCH",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_admin_filter_orders_by_status_success(client):
    seed_order(order_no="ORD-FILTER-001", order_status="Processing")

    response = client.get(
        "/admin/orders?order_status=Processing",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_admin_get_order_success(client):
    seeded = seed_order(order_no="ORD-GET-001")

    response = client.get(
        f"/admin/orders/{seeded['order_id']}",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Order retrieved successfully"
    assert body["data"]["order"]["order_id"] == seeded["order_id"]
    assert body["data"]["customer"]["customer_name"] == "Admin Order Customer"
    assert len(body["data"]["items"]) == 1


def test_admin_get_order_items_success(client):
    seeded = seed_order(order_no="ORD-ITEMS-001")

    response = client.get(
        f"/admin/orders/{seeded['order_id']}/items",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Order items retrieved successfully"
    assert body["total"] == 1
    assert body["data"][0]["product_name"] == "Admin Order Backpack"


def test_admin_update_order_status_success(client):
    seeded = seed_order(order_no="ORD-STATUS-001", order_status="Pending")

    response = client.patch(
        f"/admin/orders/{seeded['order_id']}/status",
        headers=get_admin_headers(),
        json={
            "order_status": "Processing",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Order status updated successfully"
    assert body["data"]["order"]["order_status"] == "Processing"


def test_admin_update_order_invalid_status_error(client):
    seeded = seed_order(order_no="ORD-INVALID-STATUS-001", order_status="Pending")

    response = client.patch(
        f"/admin/orders/{seeded['order_id']}/status",
        headers=get_admin_headers(),
        json={
            "order_status": "UnknownStatus",
        },
    )

    assert response.status_code == 400


def test_admin_cancel_order_success(client):
    seeded = seed_order(order_no="ORD-CANCEL-001", order_status="Pending")

    response = client.patch(
        f"/admin/orders/{seeded['order_id']}/cancel",
        headers=get_admin_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Order cancelled successfully"
    assert body["data"]["order"]["order_status"] == "Cancelled"


def test_admin_cancel_delivered_order_error(client):
    seeded = seed_order(order_no="ORD-DELIVERED-001", order_status="Delivered")

    response = client.patch(
        f"/admin/orders/{seeded['order_id']}/cancel",
        headers=get_admin_headers(),
    )

    assert response.status_code == 400


def test_admin_order_without_token_error(client):
    response = client.get("/admin/orders")

    assert response.status_code == 401


def test_admin_order_customer_role_forbidden(client):
    token = create_access_token(
        subject="2",
        extra_payload={
            "user_id": 2,
            "email": "customer@example.com",
            "role": "Customer",
        },
    )

    response = client.get(
        "/admin/orders",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
