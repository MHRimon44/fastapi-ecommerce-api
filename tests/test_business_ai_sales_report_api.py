def test_analyze_sales_report_success(client):
    response = client.post(
        "/business-ai/sales-report/analyze",
        json={
            "report_title": "Daily Sales Report",
            "start_date": "2026-06-27",
            "end_date": "2026-06-27",
            "total_orders": 10,
            "total_sales_amount": 25000,
            "total_customers": 8,
            "total_products_sold": 15,
            "previous_sales_amount": 20000,
            "sales_channels": [
                {
                    "channel_name": "Website",
                    "orders": 7,
                    "sales_amount": 18000
                },
                {
                    "channel_name": "Facebook",
                    "orders": 3,
                    "sales_amount": 7000
                }
            ],
            "top_products": [
                {
                    "product_name": "Laptop Backpack",
                    "quantity_sold": 8,
                    "sales_amount": 12000
                },
                {
                    "product_name": "Travel Bag",
                    "quantity_sold": 4,
                    "sales_amount": 8000
                }
            ],
            "note": "Sales increased after campaign."
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Sales report analyzed successfully"
    assert "Daily Sales Report" in body["data"]["summary"]
    assert body["data"]["average_order_value"] == 2500
    assert body["data"]["sales_growth_percent"] == 25
    assert body["data"]["provider"] == "mock"
    assert len(body["data"]["insights"]) >= 5
    assert len(body["data"]["recommendations"]) >= 1


def test_analyze_sales_report_validation_error(client):
    response = client.post(
        "/business-ai/sales-report/analyze",
        json={
            "report_title": "A",
            "total_orders": -1,
            "total_sales_amount": -100,
            "total_customers": -5,
            "total_products_sold": -2,
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_analyze_sales_report_negative_growth_flag(client):
    response = client.post(
        "/business-ai/sales-report/analyze",
        json={
            "report_title": "Weekly Sales Report",
            "total_orders": 5,
            "total_sales_amount": 10000,
            "total_customers": 5,
            "total_products_sold": 6,
            "previous_sales_amount": 20000,
            "sales_channels": [],
            "top_products": []
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["sales_growth_percent"] == -50
    assert "Sales dropped compared to the previous period." in body["data"]["risk_flags"]


def test_analyze_sales_report_zero_order_report(client):
    response = client.post(
        "/business-ai/sales-report/analyze",
        json={
            "report_title": "Empty Sales Report",
            "total_orders": 0,
            "total_sales_amount": 0,
            "total_customers": 0,
            "total_products_sold": 0
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["average_order_value"] == 0
    assert "No orders recorded for this report." in body["data"]["risk_flags"]
