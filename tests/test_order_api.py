def create_customer(client):
    client.post(
        "/customers",
        json={
            "customer_name": "Rahim Uddin",
            "phone": "01700000000",
            "email": "rahim@example.com",
        },
    )

    response = client.get("/customers")

    return response.json()[0]["customer_id"]


def create_product(client):
    client.post(
        "/products",
        json={
            "product_name": "iPhone 15",
            "sku": "IPHONE-15-BLK-128",
            "price": 112000,
            "stock_qty": 10,
            "description": "Apple iPhone 15",
        },
    )

    response = client.get("/products")

    return response.json()["items"][0]["product_id"]


def test_create_order_success(client):
    customer_id = create_customer(client)
    product_id = create_product(client)

    response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ],
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Order placed successfully"
    assert "order_no" in body
    assert body["order_no"] != ""


def test_order_create_reduces_product_stock(client):
    customer_id = create_customer(client)
    product_id = create_product(client)

    client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ],
        },
    )

    product_response = client.get(f"/products/{product_id}")

    assert product_response.status_code == 200
    assert product_response.json()["stock_qty"] == 8


def test_order_create_not_enough_stock_error(client):
    customer_id = create_customer(client)
    product_id = create_product(client)

    response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 999,
                }
            ],
        },
    )

    assert response.status_code == 400
    assert "message" in response.json()
