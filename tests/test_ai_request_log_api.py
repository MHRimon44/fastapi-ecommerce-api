def sales_only_payload():
    return {
        "review_title": "Sales Only Log Review",
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


def test_ai_commerce_business_review_creates_log(client):
    review_response = client.post(
        "/ai-commerce/business-review",
        json=sales_only_payload(),
    )

    assert review_response.status_code == 200

    log_response = client.get(
        "/ai-logs/recent?limit=5",
    )

    assert log_response.status_code == 200

    body = log_response.json()

    assert body["message"] == "AI request logs retrieved successfully"
    assert len(body["data"]) >= 1

    latest_log = body["data"][0]

    assert latest_log["module_name"] == "AI_COMMERCE_BUSINESS_REVIEW"
    assert latest_log["endpoint"] == "/ai-commerce/business-review"
    assert latest_log["status_code"] == 200
    assert "Sales Only Log Review" in latest_log["request_body"]
    assert "AI commerce business review generated successfully" in latest_log["response_body"]


def test_get_recent_ai_logs_limit_validation(client):
    response = client.get(
        "/ai-logs/recent?limit=0",
    )

    assert response.status_code == 422
    assert "message" in response.json()
