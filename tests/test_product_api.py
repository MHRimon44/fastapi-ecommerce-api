import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.product_repository import product_repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_repository():
    product_repository.reset()
    yield
    product_repository.reset()


def create_product(
    product_name: str = "iPhone",
    price: float = 112000,
    stock_qty: int = 10,
    description: str = "Apple product",
):
    return client.post(
        "/products",
        json={
            "product_name": product_name,
            "price": price,
            "stock_qty": stock_qty,
            "description": description,
        },
    )


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "FastAPI is running",
    }


def test_create_product_success():
    response = create_product()

    assert response.status_code == 201

    data = response.json()

    assert data["product_id"] == 1
    assert data["product_name"] == "iPhone"
    assert data["price"] == 112000
    assert data["stock_qty"] == 10
    assert data["description"] == "Apple product"


def test_create_product_without_description_success():
    response = client.post(
        "/products",
        json={
            "product_name": "Samsung",
            "price": 90000,
            "stock_qty": 5,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product_name"] == "Samsung"
    assert data["description"] is None


def test_create_product_validation_error_for_negative_price():
    response = client.post(
        "/products",
        json={
            "product_name": "Invalid Product",
            "price": -100,
            "stock_qty": 5,
        },
    )

    assert response.status_code == 422


def test_get_product_by_id_success():
    create_product(product_name="iPhone", price=112000)

    response = client.get("/products/1")

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 1
    assert data["product_name"] == "iPhone"


def test_get_product_by_id_not_found():
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_get_products_with_sort_high_to_low():
    create_product(product_name="Low Price Product", price=1000)
    create_product(product_name="High Price Product", price=5000)
    create_product(product_name="Medium Price Product", price=3000)

    response = client.get("/products?sort=high_to_low")

    assert response.status_code == 200

    data = response.json()
    items = data["items"]

    assert items[0]["price"] == 5000
    assert items[1]["price"] == 3000
    assert items[2]["price"] == 1000


def test_get_products_with_sort_low_to_high():
    create_product(product_name="High Price Product", price=5000)
    create_product(product_name="Low Price Product", price=1000)
    create_product(product_name="Medium Price Product", price=3000)

    response = client.get("/products?sort=low_to_high")

    assert response.status_code == 200

    data = response.json()
    items = data["items"]

    assert items[0]["price"] == 1000
    assert items[1]["price"] == 3000
    assert items[2]["price"] == 5000


def test_get_products_with_sort_newly_added():
    create_product(product_name="First Product", price=1000)
    create_product(product_name="Second Product", price=2000)
    create_product(product_name="Third Product", price=3000)

    response = client.get("/products?sort=newly_added")

    assert response.status_code == 200

    data = response.json()
    items = data["items"]

    assert items[0]["product_name"] == "Third Product"
    assert items[1]["product_name"] == "Second Product"
    assert items[2]["product_name"] == "First Product"


def test_get_products_with_pagination():
    create_product(product_name="Product 1", price=1000)
    create_product(product_name="Product 2", price=2000)
    create_product(product_name="Product 3", price=3000)

    response = client.get("/products?limit=2&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["limit"] == 2
    assert data["offset"] == 0
    assert len(data["items"]) == 2
    assert data["items"][0]["product_name"] == "Product 1"
    assert data["items"][1]["product_name"] == "Product 2"


def test_get_products_with_second_page():
    create_product(product_name="Product 1", price=1000)
    create_product(product_name="Product 2", price=2000)
    create_product(product_name="Product 3", price=3000)

    response = client.get("/products?limit=2&offset=2")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["limit"] == 2
    assert data["offset"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["product_name"] == "Product 3"


def test_get_products_invalid_price_range():
    response = client.get("/products?min_price=5000&max_price=1000")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "min_price cannot be greater than max_price",
    }


def test_patch_product_success():
    create_product(product_name="iPhone", price=112000, stock_qty=10)

    response = client.patch(
        "/products/1",
        json={
            "price": 110000,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 1
    assert data["product_name"] == "iPhone"
    assert data["price"] == 110000
    assert data["stock_qty"] == 10


def test_patch_product_empty_body_error():
    create_product(product_name="iPhone", price=112000, stock_qty=10)

    response = client.patch(
        "/products/1",
        json={},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "At least one field must be provided for update",
    }


def test_delete_product_success():
    create_product(product_name="iPhone", price=112000, stock_qty=10)

    delete_response = client.delete("/products/1")

    assert delete_response.status_code == 204

    get_response = client.get("/products/1")

    assert get_response.status_code == 404