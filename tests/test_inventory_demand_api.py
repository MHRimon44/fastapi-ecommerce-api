def test_inventory_demand_forecast_reorder_needed(client):
    response = client.post(
        "/business-ai/inventory-demand/forecast",
        json={
            "product_id": 1,
            "product_name": "Laptop Backpack",
            "sku": "BAG-LAP-001",
            "category": "Backpack",
            "current_stock_qty": 20,
            "reorder_point": 30,
            "lead_time_days": 7,
            "safety_stock_qty": 10,
            "forecast_days": 30,
            "incoming_stock_qty": 0,
            "sales_history": [
                {
                    "period": "day-1",
                    "quantity_sold": 5
                },
                {
                    "period": "day-2",
                    "quantity_sold": 6
                },
                {
                    "period": "day-3",
                    "quantity_sold": 4
                }
            ],
            "note": "Campaign is running."
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Inventory demand forecast generated successfully"
    assert body["data"]["product_name"] == "Laptop Backpack"
    assert body["data"]["average_daily_sales"] == 5
    assert body["data"]["forecasted_demand_qty"] == 150
    assert body["data"]["reorder_needed"] is True
    assert body["data"]["suggested_reorder_qty"] == 140
    assert body["data"]["risk_level"] in ["MEDIUM", "HIGH"]
    assert body["data"]["provider"] == "mock"


def test_inventory_demand_forecast_stock_sufficient(client):
    response = client.post(
        "/business-ai/inventory-demand/forecast",
        json={
            "product_name": "Travel Bag",
            "current_stock_qty": 500,
            "reorder_point": 50,
            "lead_time_days": 7,
            "safety_stock_qty": 20,
            "forecast_days": 30,
            "sales_history": [
                {
                    "period": "day-1",
                    "quantity_sold": 5
                },
                {
                    "period": "day-2",
                    "quantity_sold": 5
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["reorder_needed"] is False
    assert body["data"]["suggested_reorder_qty"] == 0
    assert body["data"]["risk_level"] == "LOW"


def test_inventory_demand_forecast_zero_sales_history(client):
    response = client.post(
        "/business-ai/inventory-demand/forecast",
        json={
            "product_name": "Slow Moving Item",
            "current_stock_qty": 100,
            "reorder_point": 20,
            "lead_time_days": 7,
            "safety_stock_qty": 10,
            "forecast_days": 30,
            "sales_history": [
                {
                    "period": "day-1",
                    "quantity_sold": 0
                },
                {
                    "period": "day-2",
                    "quantity_sold": 0
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["average_daily_sales"] == 0
    assert body["data"]["estimated_stock_remaining_days"] is None
    assert body["data"]["forecasted_demand_qty"] == 0


def test_inventory_demand_validation_error(client):
    response = client.post(
        "/business-ai/inventory-demand/forecast",
        json={
            "product_name": "A",
            "current_stock_qty": -1,
            "lead_time_days": 0,
            "forecast_days": 0,
            "sales_history": []
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()
