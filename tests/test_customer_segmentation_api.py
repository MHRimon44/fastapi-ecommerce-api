def test_customer_segmentation_vip_customer(client):
    response = client.post(
        "/business-ai/customer-segmentation/segment",
        json={
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
                "Backpack",
                "Travel Bag"
            ],
            "preferred_channels": [
                "Website"
            ],
            "note": "Premium customer."
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Customer segmented successfully"
    assert body["data"]["segment_name"] == "VIP_CUSTOMER"
    assert body["data"]["customer_value_level"] == "HIGH"
    assert body["data"]["segment_score"] >= 80
    assert body["data"]["provider"] == "mock"
    assert len(body["data"]["recommendations"]) >= 1


def test_customer_segmentation_churn_risk_customer(client):
    response = client.post(
        "/business-ai/customer-segmentation/segment",
        json={
            "customer_id": 2,
            "customer_name": "Karim",
            "total_orders": 8,
            "total_spent": 25000,
            "average_order_value": 3000,
            "days_since_last_order": 220,
            "return_order_count": 0,
            "cancelled_order_count": 0,
            "used_voucher_count": 2,
            "total_discount_received": 1000,
            "preferred_categories": [
                "Laptop Bag"
            ],
            "preferred_channels": [
                "Facebook"
            ]
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["segment_name"] == "CHURN_RISK_CUSTOMER"
    assert "Customer is at high churn risk." in body["data"]["risk_flags"]


def test_customer_segmentation_new_customer(client):
    response = client.post(
        "/business-ai/customer-segmentation/segment",
        json={
            "customer_id": 3,
            "customer_name": "New Customer",
            "total_orders": 1,
            "total_spent": 1500,
            "average_order_value": 1500,
            "days_since_last_order": 5,
            "return_order_count": 0,
            "cancelled_order_count": 0,
            "used_voucher_count": 1,
            "total_discount_received": 100
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["segment_name"] == "NEW_CUSTOMER"
    assert body["data"]["segment_score"] >= 0


def test_customer_segmentation_no_purchase_customer(client):
    response = client.post(
        "/business-ai/customer-segmentation/segment",
        json={
            "customer_id": 4,
            "customer_name": "Lead Customer",
            "total_orders": 0,
            "total_spent": 0,
            "average_order_value": 0,
            "days_since_last_order": None,
            "return_order_count": 0,
            "cancelled_order_count": 0,
            "used_voucher_count": 0,
            "total_discount_received": 0
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["segment_name"] == "NO_PURCHASE_CUSTOMER"
    assert body["data"]["customer_value_level"] == "LOW"


def test_customer_segmentation_validation_error(client):
    response = client.post(
        "/business-ai/customer-segmentation/segment",
        json={
            "total_orders": -1,
            "total_spent": -100,
            "average_order_value": -10,
            "return_order_count": -1,
            "cancelled_order_count": -1
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()
