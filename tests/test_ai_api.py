import pytest

from app.core.config import settings


@pytest.fixture(autouse=True)
def force_mock_ai_provider_for_tests():
    original_provider = settings.AI_PROVIDER
    original_model_name = settings.AI_MODEL_NAME

    settings.AI_PROVIDER = "mock"
    settings.AI_MODEL_NAME = "mock-product-writer-v1"

    yield

    settings.AI_PROVIDER = original_provider
    settings.AI_MODEL_NAME = original_model_name


def test_generate_product_description_success(client):
    response = client.post(
        "/ai/generate-product-description",
        json={
            "product_name": "Laptop Backpack",
            "features": [
                "water resistant",
                "15 inch laptop compartment",
                "lightweight design",
            ],
            "target_audience": "office professionals",
            "tone": "premium",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Product description generated successfully"
    assert body["data"]["provider"] == "mock"
    assert "Laptop Backpack" in body["data"]["description"]
    assert len(body["data"]["bullet_points"]) == 3


def test_generate_product_description_validation_error(client):
    response = client.post(
        "/ai/generate-product-description",
        json={
            "product_name": "A",
            "features": [],
            "tone": "p",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_summarize_order_report_success(client):
    response = client.post(
        "/ai/summarize-order-report",
        json={
            "report_title": "Daily Sales Report",
            "total_orders": 10,
            "total_sales_amount": 25000,
            "total_customers": 8,
            "top_products": [
                "Laptop Backpack",
                "Travel Bag",
            ],
            "note": "Sales increased due to campaign.",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Order report summarized successfully"
    assert body["data"]["provider"] == "mock"
    assert "Daily Sales Report" in body["data"]["summary"]
    assert len(body["data"]["insights"]) >= 3


def test_summarize_order_report_validation_error(client):
    response = client.post(
        "/ai/summarize-order-report",
        json={
            "report_title": "A",
            "total_orders": -1,
            "total_sales_amount": -100,
            "total_customers": -5,
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_customer_support_reply_success(client):
    response = client.post(
        "/ai/customer-support-reply",
        json={
            "customer_name": "Rahim Uddin",
            "order_no": "ORD-1001",
            "customer_message": "I want to know my delivery update.",
            "tone": "polite",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Customer support reply generated successfully"
    assert body["data"]["provider"] == "mock"
    assert "Rahim Uddin" in body["data"]["reply"]
    assert "ORD-1001" in body["data"]["reply"]
    assert len(body["data"]["suggested_actions"]) > 0


def test_customer_support_reply_validation_error(client):
    response = client.post(
        "/ai/customer-support-reply",
        json={
            "customer_message": "Bad",
            "tone": "p",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()
