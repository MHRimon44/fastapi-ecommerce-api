def register_user(client):
    return client.post(
        "/auth/register",
        json={
            "full_name": "Rahim Uddin",
            "email": "rahim@example.com",
            "phone": "01700000000",
            "password": "123456",
        },
    )


def login_user(client):
    return client.post(
        "/auth/login",
        json={
            "email": "rahim@example.com",
            "password": "123456",
        },
    )


def test_register_user_success(client):
    response = register_user(client)

    assert response.status_code == 201
    assert response.json() == {
        "message": "User registered successfully",
    }


def test_login_user_success(client):
    register_response = register_user(client)

    assert register_response.status_code == 201

    response = login_user(client)

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["access_token"] != ""


def test_auth_me_without_token_error(client):
    response = client.get("/auth/me")

    assert response.status_code in [401, 403]


def test_auth_me_with_token_success(client):
    register_response = register_user(client)

    assert register_response.status_code == 201

    login_response = login_user(client)

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == "rahim@example.com"
    assert body["phone"] == "01700000000"