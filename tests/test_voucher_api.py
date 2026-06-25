from datetime import datetime, timedelta


def create_voucher_payload(
    code: str = "SAVE100",
    discount_type: str = "FLAT",
    discount_value: float = 100,
    min_order_amount: float = 500,
    max_discount_amount: float = 100,
    usage_limit: int = 10,
):
    now = datetime.utcnow()

    return {
        "code": code,
        "discount_type": discount_type,
        "discount_value": discount_value,
        "min_order_amount": min_order_amount,
        "max_discount_amount": max_discount_amount,
        "usage_limit": usage_limit,
        "start_at": (now - timedelta(days=1)).isoformat(),
        "end_at": (now + timedelta(days=7)).isoformat(),
    }


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


def create_product(client, price: float = 112000, stock_qty: int = 10):
    client.post(
        "/products",
        json={
            "product_name": "iPhone 15",
            "sku": "IPHONE-15-BLK-128",
            "price": price,
            "stock_qty": stock_qty,
            "description": "Apple iPhone 15",
        },
    )

    response = client.get("/products")
    return response.json()["items"][0]["product_id"]


def create_order_and_get_id(client, quantity: int = 1):
    customer_id = create_customer(client)
    product_id = create_product(client)

    order_response = client.post(
        "/orders",
        json={
            "customer_id": customer_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": quantity,
                }
            ],
        },
    )

    assert order_response.status_code == 201

    order_no = order_response.json()["order_no"]

    orders_response = client.get("/orders")
    assert orders_response.status_code == 200

    body = orders_response.json()

    if isinstance(body, list):
        orders = body
    else:
        orders = body.get("items", [])

    for order in orders:
        if order.get("order_no") == order_no:
            return order["order_id"]

    raise AssertionError("Created order was not found in GET /orders response")


def test_create_voucher_success(client):
    response = client.post(
        "/vouchers",
        json=create_voucher_payload(),
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Voucher created successfully",
    }


def test_create_duplicate_voucher_error(client):
    client.post(
        "/vouchers",
        json=create_voucher_payload(code="SAVE100"),
    )

    response = client.post(
        "/vouchers",
        json=create_voucher_payload(code="SAVE100"),
    )

    assert response.status_code == 400
    assert "message" in response.json()


def test_apply_voucher_success(client):
    order_id = create_order_and_get_id(client)

    client.post(
        "/vouchers",
        json=create_voucher_payload(
            code="SAVE100",
            min_order_amount=500,
        ),
    )

    response = client.post(
        "/vouchers/apply",
        json={
            "order_id": order_id,
            "voucher_code": "SAVE100",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Voucher applied successfully",
    }


def test_apply_voucher_invalid_code_error(client):
    order_id = create_order_and_get_id(client)

    response = client.post(
        "/vouchers/apply",
        json={
            "order_id": order_id,
            "voucher_code": "WRONGCODE",
        },
    )

    assert response.status_code == 404
    assert "message" in response.json()


def test_apply_voucher_minimum_order_amount_error(client):
    order_id = create_order_and_get_id(client)

    client.post(
        "/vouchers",
        json=create_voucher_payload(
            code="SAVE100",
            min_order_amount=999999,
        ),
    )

    response = client.post(
        "/vouchers/apply",
        json={
            "order_id": order_id,
            "voucher_code": "SAVE100",
        },
    )

    assert response.status_code == 400
    assert "message" in response.json()