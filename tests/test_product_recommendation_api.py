def test_product_recommendation_success(client):
    response = client.post(
        "/business-ai/product-recommendations/recommend",
        json={
            "customer_id": 1,
            "customer_segment": "office_professional",
            "preferred_categories": [
                "Backpack"
            ],
            "preferred_features": [
                "laptop compartment",
                "water resistant"
            ],
            "previous_purchase_categories": [
                "Backpack"
            ],
            "budget_min": 1000,
            "budget_max": 2000,
            "use_case": "office laptop daily commute",
            "top_k": 2,
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
                        "15 inch laptop compartment",
                        "water resistant fabric",
                        "lightweight design"
                    ],
                    "tags": [
                        "office",
                        "laptop",
                        "commute"
                    ]
                },
                {
                    "product_id": 2,
                    "product_name": "Travel Duffel Bag",
                    "sku": "BAG-TRV-001",
                    "category": "Travel Bag",
                    "description": "Large travel bag for short trips.",
                    "price": 2200,
                    "stock_qty": 50,
                    "rating": 4.2,
                    "sales_count": 20,
                    "features": [
                        "large capacity"
                    ],
                    "tags": [
                        "travel"
                    ]
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Product recommendations generated successfully"
    assert len(body["data"]["recommended_products"]) >= 1
    assert body["data"]["recommended_products"][0]["product_name"] == "Laptop Backpack"
    assert body["data"]["recommended_products"][0]["recommendation_score"] > 0
    assert body["data"]["provider"] == "mock"


def test_product_recommendation_validation_error(client):
    response = client.post(
        "/business-ai/product-recommendations/recommend",
        json={
            "top_k": 0,
            "products": []
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_product_recommendation_excludes_out_of_stock_products(client):
    response = client.post(
        "/business-ai/product-recommendations/recommend",
        json={
            "preferred_categories": [
                "Backpack"
            ],
            "top_k": 3,
            "products": [
                {
                    "product_id": 1,
                    "product_name": "Out of Stock Backpack",
                    "category": "Backpack",
                    "description": "Backpack with laptop compartment.",
                    "price": 1500,
                    "stock_qty": 0,
                    "features": [
                        "laptop compartment"
                    ]
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["recommended_products"] == []
    assert "No suitable products found" in body["data"]["summary"]


def test_product_recommendation_respects_top_k(client):
    response = client.post(
        "/business-ai/product-recommendations/recommend",
        json={
            "preferred_categories": [
                "Backpack"
            ],
            "top_k": 1,
            "products": [
                {
                    "product_id": 1,
                    "product_name": "Laptop Backpack",
                    "category": "Backpack",
                    "description": "Office laptop backpack.",
                    "price": 1500,
                    "stock_qty": 10,
                    "features": [
                        "laptop compartment"
                    ]
                },
                {
                    "product_id": 2,
                    "product_name": "School Backpack",
                    "category": "Backpack",
                    "description": "Backpack for students.",
                    "price": 900,
                    "stock_qty": 10,
                    "features": [
                        "lightweight"
                    ]
                }
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["data"]["recommended_products"]) == 1
