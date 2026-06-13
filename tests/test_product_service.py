import pytest
from fastapi import HTTPException, status

from app.repositories.product_repository import product_repository
from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductPatchRequest,
    ProductSortOption,
    ProductUpdateRequest,
)
from app.services.product_service import product_service


@pytest.fixture(autouse=True)
def reset_repository():
    product_repository.reset()
    yield
    product_repository.reset()


def create_product_request(
    product_name: str = "iPhone",
    price: float = 112000,
    stock_qty: int = 10,
    description: str = "Apple product",
) -> ProductCreateRequest:
    return ProductCreateRequest(
        product_name=product_name,
        price=price,
        stock_qty=stock_qty,
        description=description,
    )


def test_create_product_success():
    request = create_product_request()

    product = product_service.create_product(request)

    assert product.product_id == 1
    assert product.product_name == "iPhone"
    assert product.price == 112000
    assert product.stock_qty == 10
    assert product.description == "Apple product"


def test_get_product_by_id_success():
    created_product = product_service.create_product(
        create_product_request(product_name="Samsung", price=90000)
    )

    product = product_service.get_product_by_id(created_product.product_id)

    assert product.product_id == created_product.product_id
    assert product.product_name == "Samsung"


def test_get_product_by_id_not_found():
    with pytest.raises(HTTPException) as error:
        product_service.get_product_by_id(999)

    assert error.value.status_code == status.HTTP_404_NOT_FOUND
    assert error.value.detail == "Product not found"


def test_get_products_with_search():
    product_service.create_product(
        create_product_request(product_name="iPhone 15", price=112000)
    )
    product_service.create_product(
        create_product_request(product_name="Samsung S24", price=90000)
    )

    result = product_service.get_products(
        search="iphone",
        min_price=None,
        max_price=None,
        limit=10,
        offset=0,
        sort=ProductSortOption.default,
    )

    assert result.total == 1
    assert result.items[0].product_name == "iPhone 15"


def test_get_products_with_price_filter():
    product_service.create_product(
        create_product_request(product_name="Low Price Product", price=1000)
    )
    product_service.create_product(
        create_product_request(product_name="High Price Product", price=5000)
    )

    result = product_service.get_products(
        search=None,
        min_price=2000,
        max_price=6000,
        limit=10,
        offset=0,
        sort=ProductSortOption.default,
    )

    assert result.total == 1
    assert result.items[0].product_name == "High Price Product"


def test_get_products_invalid_price_range():
    with pytest.raises(HTTPException) as error:
        product_service.get_products(
            search=None,
            min_price=5000,
            max_price=1000,
            limit=10,
            offset=0,
            sort=ProductSortOption.default,
        )

    assert error.value.status_code == status.HTTP_400_BAD_REQUEST
    assert error.value.detail == "min_price cannot be greater than max_price"


def test_get_products_sort_high_to_low():
    product_service.create_product(
        create_product_request(product_name="Low", price=1000)
    )
    product_service.create_product(
        create_product_request(product_name="High", price=5000)
    )
    product_service.create_product(
        create_product_request(product_name="Medium", price=3000)
    )

    result = product_service.get_products(
        search=None,
        min_price=None,
        max_price=None,
        limit=10,
        offset=0,
        sort=ProductSortOption.high_to_low,
    )

    assert result.items[0].price == 5000
    assert result.items[1].price == 3000
    assert result.items[2].price == 1000


def test_get_products_sort_low_to_high():
    product_service.create_product(
        create_product_request(product_name="High", price=5000)
    )
    product_service.create_product(
        create_product_request(product_name="Low", price=1000)
    )
    product_service.create_product(
        create_product_request(product_name="Medium", price=3000)
    )

    result = product_service.get_products(
        search=None,
        min_price=None,
        max_price=None,
        limit=10,
        offset=0,
        sort=ProductSortOption.low_to_high,
    )

    assert result.items[0].price == 1000
    assert result.items[1].price == 3000
    assert result.items[2].price == 5000


def test_get_products_sort_newly_added():
    product_service.create_product(
        create_product_request(product_name="First", price=1000)
    )
    product_service.create_product(
        create_product_request(product_name="Second", price=2000)
    )
    product_service.create_product(
        create_product_request(product_name="Third", price=3000)
    )

    result = product_service.get_products(
        search=None,
        min_price=None,
        max_price=None,
        limit=10,
        offset=0,
        sort=ProductSortOption.newly_added,
    )

    assert result.items[0].product_name == "Third"
    assert result.items[1].product_name == "Second"
    assert result.items[2].product_name == "First"


def test_get_products_with_pagination():
    product_service.create_product(
        create_product_request(product_name="Product 1", price=1000)
    )
    product_service.create_product(
        create_product_request(product_name="Product 2", price=2000)
    )
    product_service.create_product(
        create_product_request(product_name="Product 3", price=3000)
    )

    result = product_service.get_products(
        search=None,
        min_price=None,
        max_price=None,
        limit=2,
        offset=1,
        sort=ProductSortOption.default,
    )

    assert result.total == 3
    assert result.limit == 2
    assert result.offset == 1
    assert len(result.items) == 2
    assert result.items[0].product_name == "Product 2"
    assert result.items[1].product_name == "Product 3"


def test_update_product_success():
    product_service.create_product(
        create_product_request(product_name="Old Product", price=1000)
    )

    update_request = ProductUpdateRequest(
        product_name="Updated Product",
        price=2000,
        stock_qty=20,
        description="Updated description",
    )

    updated_product = product_service.update_product(1, update_request)

    assert updated_product.product_id == 1
    assert updated_product.product_name == "Updated Product"
    assert updated_product.price == 2000
    assert updated_product.stock_qty == 20
    assert updated_product.description == "Updated description"


def test_patch_product_success():
    product_service.create_product(
        create_product_request(product_name="iPhone", price=112000, stock_qty=10)
    )

    patch_request = ProductPatchRequest(price=110000)

    updated_product = product_service.patch_product(1, patch_request)

    assert updated_product.product_id == 1
    assert updated_product.product_name == "iPhone"
    assert updated_product.price == 110000
    assert updated_product.stock_qty == 10


def test_patch_product_empty_body_error():
    product_service.create_product(
        create_product_request(product_name="iPhone", price=112000)
    )

    patch_request = ProductPatchRequest()

    with pytest.raises(HTTPException) as error:
        product_service.patch_product(1, patch_request)

    assert error.value.status_code == status.HTTP_400_BAD_REQUEST
    assert error.value.detail == "At least one field must be provided for update"


def test_delete_product_success():
    product_service.create_product(
        create_product_request(product_name="iPhone", price=112000)
    )

    product_service.delete_product(1)

    with pytest.raises(HTTPException) as error:
        product_service.get_product_by_id(1)

    assert error.value.status_code == status.HTTP_404_NOT_FOUND