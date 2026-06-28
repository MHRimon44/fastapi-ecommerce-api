from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from jose import jwt

from app.core.config import settings
from app.dependencies.auth_guard import require_authenticated_user, require_admin_user
from app.main import app


def create_token(role="Customer", token_type="access"):
    payload = {
        "sub": "test@example.com",
        "email": "test@example.com",
        "user_id": 1,
        "role": role,
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def test_admin_users_requires_authentication():
    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)

    client = TestClient(app)

    response = client.get("/admin/users")

    assert response.status_code in [401, 403]


def test_admin_users_rejects_customer_role():
    app.dependency_overrides.pop(require_authenticated_user, None)
    app.dependency_overrides.pop(require_admin_user, None)

    client = TestClient(app)

    token = create_token(role="Customer")

    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 403


def test_refresh_rejects_access_token():
    client = TestClient(app)

    token = create_token(role="Admin", token_type="access")

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": token
        },
    )

    assert response.status_code == 401


def test_refresh_accepts_refresh_token():
    client = TestClient(app)

    token = create_token(role="Admin", token_type="refresh")

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": token
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Token refreshed successfully"
    assert body["data"]["access_token"]
    assert body["data"]["refresh_token"]
