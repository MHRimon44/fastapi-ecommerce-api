from app.api.v1 import order_routes


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


def test_order_create_calls_background_tasks(client, monkeypatch):
    called_tasks = []

    def fake_order_confirmation_task(order_no: str):
        called_tasks.append(
            {
                "task": "order_confirmation",
                "order_no": order_no,
            }
        )

    def fake_send_email_task(to_email: str, subject: str, body: str):
        called_tasks.append(
            {
                "task": "email",
                "to_email": to_email,
                "subject": subject,
                "body": body,
            }
        )

    def fake_enqueue_notification_task(channel: str, message: str):
        called_tasks.append(
            {
                "task": "notification",
                "channel": channel,
                "message": message,
            }
        )

    monkeypatch.setattr(
        order_routes,
        "send_order_confirmation_notification",
        fake_order_confirmation_task,
    )

    monkeypatch.setattr(
        order_routes,
        "send_email_task",
        fake_send_email_task,
    )

    monkeypatch.setattr(
        order_routes,
        "enqueue_notification_task",
        fake_enqueue_notification_task,
    )

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

    order_no = response.json()["order_no"]

    assert len(called_tasks) == 3

    assert called_tasks[0]["task"] == "order_confirmation"
    assert called_tasks[0]["order_no"] == order_no

    assert called_tasks[1]["task"] == "email"
    assert order_no in called_tasks[1]["body"]

    assert called_tasks[2]["task"] == "notification"
