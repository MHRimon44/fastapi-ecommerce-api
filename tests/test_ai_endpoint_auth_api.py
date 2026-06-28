from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.dependencies.auth_guard import require_authenticated_user
from app.main import app


def create_test_token():
    payload = {
        "sub": "test@example.com",
        "email": "test@example.com",
        "user_id": 1,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def sales_only_payload():
    return {
        "review_title": "Sales Only Auth Review",
        "sales_report": {
            "report_title": "Daily Sales Report",
            "total_orders": 10,
            "total_sales_amount": 25000,
            "total_customers": 8,
            "total_products_sold": 15,
            "previous_sales_amount": 20000,
            "sales_channels": [],
            "top_products": [],
        },
    }


def test_ai_commerce_endpoint_requires_authentication():
    app.dependency_overrides.pop(require_authenticated_user, None)

    no_auth_client = TestClient(app)

    response = no_auth_client.post(
        "/ai-commerce/business-review",
        json=sales_only_payload(),
    )

    assert response.status_code == 401


def test_ai_commerce_endpoint_rejects_invalid_token():
    app.dependency_overrides.pop(require_authenticated_user, None)

    no_auth_client = TestClient(app)

    response = no_auth_client.post(
        "/ai-commerce/business-review",
        json=sales_only_payload(),
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_ai_commerce_endpoint_accepts_valid_token():
    app.dependency_overrides.pop(require_authenticated_user, None)

    no_auth_client = TestClient(app)

    token = create_test_token()

    response = no_auth_client.post(
        "/ai-commerce/business-review",
        json=sales_only_payload(),
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "AI commerce business review generated successfully"
