def test_ai_commerce_business_review_success(client):
    response = client.post(
        "/ai-commerce/business-review",
        json={
            "review_title": "Daily AI Commerce Review",
            "sales_report": {
                "report_title": "Daily Sales Report",
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
                    }
                ],
                "top_products": [
                    {
                        "product_name": "Laptop Backpack",
                        "quantity_sold": 8,
                        "sales_amount": 12000
                    }
                ]
            },
            "voucher_fraud": {
                "voucher_code": "MEGA50",
                "discount_type": "PERCENTAGE",
                "discount_value": 50,
                "min_order_amount": 500,
                "max_discount_amount": 1000,
                "usage_limit": 100,
                "used_count": 100,
                "total_orders_using_voucher": 100,
                "total_discount_given": 60000,
                "total_sales_amount": 100000,
                "unique_customers_used": 20,
                "repeated_customers_count": 60,
                "suspicious_order_count": 4,
                "customer_patterns": [
                    {
                        "customer_id": 1,
                        "customer_name": "Rahim",
                        "usage_count": 7,
                        "total_discount_amount": 7000,
                        "total_order_amount": 10000
                    }
                ]
            },
            "product_recommendation": {
                "preferred_categories": [
                    "Backpack"
                ],
                "preferred_features": [
                    "laptop compartment"
                ],
                "budget_min": 1000,
                "budget_max": 2000,
                "use_case": "office laptop daily commute",
                "top_k": 1,
                "products": [
                    {
                        "product_id": 1,
                        "product_name": "Laptop Backpack",
                        "sku": "BAG-LAP-001",
                        "category": "Backpack",
                        "description": "Professional backpack for office laptop users.",
                        "price": 1599,
                        "stock_qty": 100,
                        "rating": 4.7,
                        "sales_count": 80,
                        "features": [
                            "15 inch laptop compartment"
                        ],
                        "tags": [
                            "office",
                            "laptop"
                        ]
                    }
                ]
            },
            "inventory_forecasts": [
                {
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
                    ]
                }
            ],
            "customer_segments": [
                {
                    "customer_id": 1,
                    "customer_name": "Rahim",
                    "total_orders": 25,
                    "total_spent": 120000,
                    "average_order_value": 6000,
                    "days_since_last_order": 10,
                    "return_order_count": 1,
                    "cancelled_order_count": 0,
                    "used_voucher_count": 5,
                    "total_discount_received": 3000,
                    "preferred_categories": [
                        "Backpack"
                    ],
                    "preferred_channels": [
                        "Website"
                    ]
                }
            ],
            "note": "Review before campaign scaling."
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "AI commerce business review generated successfully"
    assert body["data"]["review_title"] == "Daily AI Commerce Review"
    assert body["data"]["overall_risk_level"] == "HIGH"
    assert len(body["data"]["module_summaries"]) == 5
    assert len(body["data"]["final_action_plan"]) >= 1
    assert body["data"]["provider"] == "mock"


def test_ai_commerce_business_review_sales_only(client):
    response = client.post(
        "/ai-commerce/business-review",
        json={
            "review_title": "Sales Only Review",
            "sales_report": {
                "report_title": "Daily Sales Report",
                "total_orders": 10,
                "total_sales_amount": 25000,
                "total_customers": 8,
                "total_products_sold": 15,
                "previous_sales_amount": 20000,
                "sales_channels": [],
                "top_products": []
            }
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["review_title"] == "Sales Only Review"
    assert len(body["data"]["module_summaries"]) == 1
    assert body["data"]["module_summaries"][0]["module_name"] == "Sales Report"


def test_ai_commerce_business_review_requires_one_module(client):
    response = client.post(
        "/ai-commerce/business-review",
        json={
            "review_title": "Empty Review"
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_ai_commerce_business_review_inventory_high_risk(client):
    response = client.post(
        "/ai-commerce/business-review",
        json={
            "review_title": "Inventory Risk Review",
            "inventory_forecasts": [
                {
                    "product_name": "Laptop Backpack",
                    "current_stock_qty": 0,
                    "reorder_point": 20,
                    "lead_time_days": 7,
                    "safety_stock_qty": 10,
                    "forecast_days": 30,
                    "sales_history": [
                        {
                            "period": "day-1",
                            "quantity_sold": 5
                        }
                    ]
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["overall_risk_level"] == "HIGH"
    assert body["data"]["module_summaries"][0]["module_name"] == "Inventory Demand"
    assert len(body["data"]["module_summaries"][0]["risk_flags"]) >= 1
