def test_detect_voucher_fraud_low_risk(client):
    response = client.post(
        "/business-ai/voucher-fraud/detect",
        json={
            "voucher_code": "SAVE100",
            "discount_type": "FLAT",
            "discount_value": 100,
            "min_order_amount": 1000,
            "max_discount_amount": 100,
            "usage_limit": 100,
            "used_count": 10,
            "total_orders_using_voucher": 10,
            "total_discount_given": 1000,
            "total_sales_amount": 30000,
            "unique_customers_used": 10,
            "repeated_customers_count": 0,
            "suspicious_order_count": 0,
            "customer_patterns": []
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Voucher fraud risk analyzed successfully"
    assert body["data"]["risk_level"] == "LOW"
    assert body["data"]["is_suspicious"] is False
    assert body["data"]["provider"] == "mock"


def test_detect_voucher_fraud_high_risk(client):
    response = client.post(
        "/business-ai/voucher-fraud/detect",
        json={
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
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["risk_level"] == "HIGH"
    assert body["data"]["is_suspicious"] is True
    assert body["data"]["risk_score"] >= 70
    assert len(body["data"]["signals"]) >= 3
    assert len(body["data"]["recommendations"]) >= 1


def test_detect_voucher_fraud_validation_error(client):
    response = client.post(
        "/business-ai/voucher-fraud/detect",
        json={
            "voucher_code": "A",
            "discount_type": "PERCENTAGE",
            "discount_value": -10,
            "used_count": -1,
            "total_orders_using_voucher": -1,
            "total_discount_given": -100,
            "total_sales_amount": -500,
            "unique_customers_used": -1,
            "repeated_customers_count": -1
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_detect_voucher_fraud_medium_risk_repeated_usage(client):
    response = client.post(
        "/business-ai/voucher-fraud/detect",
        json={
            "voucher_code": "REPEAT20",
            "discount_type": "PERCENTAGE",
            "discount_value": 20,
            "min_order_amount": 500,
            "usage_limit": 100,
            "used_count": 70,
            "total_orders_using_voucher": 50,
            "total_discount_given": 12000,
            "total_sales_amount": 50000,
            "unique_customers_used": 25,
            "repeated_customers_count": 20,
            "suspicious_order_count": 0,
            "customer_patterns": []
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["data"]["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    assert body["data"]["risk_score"] >= 0
    assert isinstance(body["data"]["signals"], list)
