def test_create_customer_success(client):
    response = client.post(
        "/customers",
        json={
            "customer_name": "Rahim Uddin",
            "phone": "01700000000",
            "email": "rahim@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Customer created successfully",
    }


def test_create_customer_invalid_bd_phone(client):
    response = client.post(
        "/customers",
        json={
            "customer_name": "Rahim Uddin",
            "phone": "12345",
            "email": "rahim@example.com",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "message": "Phone number must be a valid Bangladeshi mobile number. Example: 01700000000",
    }


def test_create_customer_invalid_email(client):
    response = client.post(
        "/customers",
        json={
            "customer_name": "Rahim Uddin",
            "phone": "01700000000",
            "email": "wrong-email",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "message": "Email address must be in a valid format. Example: customer@example.com",
    }


def test_get_customers_short_list(client):
    client.post(
        "/customers",
        json={
            "customer_name": "Rahim Uddin",
            "phone": "01700000000",
            "email": "rahim@example.com",
        },
    )

    response = client.get("/customers")

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["customer_name"] == "Rahim Uddin"
    assert "customer_id" in body[0]

    assert "phone" not in body[0]
    assert "email" not in body[0]