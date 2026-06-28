import pytest

from app.dependencies.auth_guard import (
    AuthenticatedUser,
    require_admin_user,
)
from app.main import app


@pytest.fixture(autouse=True)
def override_admin_dependency():
    def fake_admin_user():
        return AuthenticatedUser(
            user_id="1",
            email="admin@example.com",
            role="Admin",
            token_subject="1",
        )

    app.dependency_overrides[require_admin_user] = fake_admin_user
    yield
    app.dependency_overrides.pop(require_admin_user, None)


def test_dashboard_report_success(client):
    response = client.get("/admin/reports/dashboard")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Dashboard report retrieved successfully"
    assert "total_products" in body["data"]
    assert "total_customers" in body["data"]
    assert "total_orders" in body["data"]
    assert "total_sales_amount" in body["data"]
    assert "low_stock_products" in body["data"]


def test_sales_summary_report_success(client):
    response = client.get("/admin/reports/sales-summary")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Sales summary report retrieved successfully"
    assert "total_orders" in body["data"]
    assert "total_sales_amount" in body["data"]
    assert "average_order_value" in body["data"]
    assert isinstance(body["data"]["by_status"], list)
    assert isinstance(body["data"]["by_payment_method"], list)


def test_product_performance_report_success(client):
    response = client.get("/admin/reports/product-performance?limit=5")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Product performance report retrieved successfully"
    assert isinstance(body["data"], list)


def test_product_performance_limit_validation(client):
    response = client.get("/admin/reports/product-performance?limit=0")

    assert response.status_code == 422
    assert "message" in response.json()


def test_voucher_usage_report_success(client):
    response = client.get("/admin/reports/voucher-usage?limit=5")

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Voucher usage report retrieved successfully"
    assert isinstance(body["data"], list)
