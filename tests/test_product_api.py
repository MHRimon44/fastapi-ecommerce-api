def create_product(
    client,
    product_name: str = "iPhone 15",
    sku: str = "IPHONE-15-BLK-128",
    price: float = 112000,
    stock_qty: int = 10,
    description: str = "Apple iPhone 15",
):
    return client.post(
        "/products",
        json={
            "product_name": product_name,
            "sku": sku,
            "price": price,
            "stock_qty": stock_qty,
            "description": description,
        },
    )


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "FastAPI is running",
    }


def test_create_product_success(client):
    response = create_product(client)

    assert response.status_code == 201
    assert response.json() == {
        "message": "Product created successfully",
    }


def test_create_product_without_description_success(client):
    response = client.post(
        "/products",
        json={
            "product_name": "Samsung S24",
            "sku": "SAMSUNG-S24",
            "price": 95000,
            "stock_qty": 5,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "Product created successfully",
    }


def test_create_product_invalid_price(client):
    response = client.post(
        "/products",
        json={
            "product_name": "Invalid Product",
            "sku": "INVALID-001",
            "price": -10,
            "stock_qty": 5,
            "description": "Invalid price product",
        },
    )

    assert response.status_code == 422
    assert "message" in response.json()


def test_get_products_after_create(client):
    create_product(client)

    response = client.get("/products")

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 1
    assert body["limit"] == 10
    assert body["offset"] == 0
    assert len(body["items"]) == 1
    assert body["items"][0]["product_name"] == "iPhone 15"
    assert body["items"][0]["sku"] == "IPHONE-15-BLK-128"


def test_get_product_by_id_success(client):
    create_product(client)

    list_response = client.get("/products")
    product_id = list_response.json()["items"][0]["product_id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["product_name"] == "iPhone 15"


def test_get_product_by_id_not_found(client):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "message": "Product not found",
    }


def test_get_products_with_sort_high_to_low(client):
    create_product(
        client,
        product_name="Low Price Product",
        sku="LOW-001",
        price=100,
    )
    create_product(
        client,
        product_name="High Price Product",
        sku="HIGH-001",
        price=500,
    )

    response = client.get("/products?sort=high_to_low")

    assert response.status_code == 200

    items = response.json()["items"]

    assert items[0]["price"] == 500
    assert items[1]["price"] == 100


def test_get_products_with_sort_low_to_high(client):
    create_product(
        client,
        product_name="High Price Product",
        sku="HIGH-001",
        price=500,
    )
    create_product(
        client,
        product_name="Low Price Product",
        sku="LOW-001",
        price=100,
    )

    response = client.get("/products?sort=low_to_high")

    assert response.status_code == 200

    items = response.json()["items"]

    assert items[0]["price"] == 100
    assert items[1]["price"] == 500


def test_get_products_with_sort_newly_added(client):
    create_product(
        client,
        product_name="First Product",
        sku="FIRST-001",
        price=100,
    )
    create_product(
        client,
        product_name="Second Product",
        sku="SECOND-001",
        price=200,
    )

    response = client.get("/products?sort=newly_added")

    assert response.status_code == 200

    items = response.json()["items"]

    assert items[0]["product_name"] == "Second Product"
    assert items[1]["product_name"] == "First Product"


def test_get_products_with_pagination(client):
    for index in range(15):
        create_product(
            client,
            product_name=f"Product {index}",
            sku=f"SKU-{index}",
            price=100 + index,
        )

    response = client.get("/products?limit=5&offset=0")

    assert response.status_code == 200

    body = response.json()

    assert body["total"] == 15
    assert body["limit"] == 5
    assert body["offset"] == 0
    assert len(body["items"]) == 5


def test_get_products_invalid_price_range(client):
    response = client.get("/products?min_price=5000&max_price=1000")

    assert response.status_code == 400
    assert response.json() == {
        "message": "min_price cannot be greater than max_price",
    }


def test_patch_product_success(client):
    create_product(
        client,
        product_name="Old Product",
        sku="OLD-001",
        price=100,
    )

    list_response = client.get("/products")
    product_id = list_response.json()["items"][0]["product_id"]

    response = client.patch(
        f"/products/{product_id}",
        json={
            "price": 150,
        },
    )

    assert response.status_code == 200
    assert response.json()["price"] == 150


def test_patch_product_empty_body_error(client):
    create_product(
        client,
        product_name="Old Product",
        sku="OLD-001",
        price=100,
    )

    list_response = client.get("/products")
    product_id = list_response.json()["items"][0]["product_id"]

    response = client.patch(
        f"/products/{product_id}",
        json={},
    )

    assert response.status_code == 400
    assert response.json() == {
        "message": "At least one field must be provided for update",
    }


def test_delete_product_success(client):
    create_product(
        client,
        product_name="Delete Product",
        sku="DELETE-001",
        price=100,
    )

    list_response = client.get("/products")
    product_id = list_response.json()["items"][0]["product_id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204

    get_response = client.get(f"/products/{product_id}")

    assert get_response.status_code == 404