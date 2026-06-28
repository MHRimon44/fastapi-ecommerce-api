import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.db.session import get_session

# Import all models before create_all()
from app.models.product_model import Product
from app.models.customer_model import Customer
from app.models.order_model import Order, OrderItem
from app.models.user_model import User
from app.models.payment_model import Payment
from app.models.voucher_model import Voucher

from app.main import app


@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

from app.dependencies.auth_guard import AuthenticatedUser, require_authenticated_user


@pytest.fixture(autouse=True)
def override_ai_auth_dependency_for_tests():
    def fake_authenticated_user():
        return AuthenticatedUser(
            user_id="1",
            email="test@example.com",
            token_subject="test@example.com",
        )

    app.dependency_overrides[require_authenticated_user] = fake_authenticated_user

    yield

    app.dependency_overrides.pop(require_authenticated_user, None)

from app.dependencies.auth_guard import AuthenticatedUser, require_authenticated_user


@pytest.fixture(autouse=True)
def override_ai_auth_dependency_for_tests():
    def fake_authenticated_user():
        return AuthenticatedUser(
            user_id="1",
            email="test@example.com",
            token_subject="test@example.com",
        )

    app.dependency_overrides[require_authenticated_user] = fake_authenticated_user

    yield

    app.dependency_overrides.pop(require_authenticated_user, None)
