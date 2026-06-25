import pytest
from fastapi import HTTPException, status

from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductPatchRequest,
    ProductSortOption,
)
from app.services.product_service import product_service


def create_product_request(
    product_name: str = "iPhone",
    sku: str = "IPHONE-001",
    price: float = 112000,
    stock_qty: int = 10,
    description: str = "Apple product",
) -> ProductCreateRequest:
    return ProductCreateRequest(
        product_name=product_name,
        sku=sku,
        price=price,
        stock_qty=stock_qty,
        description=description,
    )


def test_create_product_success(session):
    request = create_product_request()

    product = product_service.create_product(
        session=session,
        request=request,
    )

    assert product.product_name == "iPhone"
    assert product.sku == "IPHONE-001"
    assert product.price == 112000
    assert product.stock_qty == 10
    assert product.description == "Apple product"


def test_get_product_by_id_success(session):
    created_product = product_service.create_product(
        session=session,
        request=create_product_request(
            product_name="Samsung",
            sku="SAMSUNG-001",
            price=90000,
        ),
    )

    product = product_service.get_product_by_id(
        session=session,
        product_id=created_product.product_id,
    )

    assert product.product_id == created_product.product_id
    assert product.product_name == "Samsung"


def test_get_product_by_id_not_found(session):
    with pytest.raises(HTTPException) as error:
        product_service.get_product_by_id(
            session=session,
            product_id=999,
        )

    assert error.value.status_code == status.HTTP_404_NOT_FOUND
    assert error.value.detail == "Product not found"


def test_get_products_invalid_price_range(session):
    with pytest.raises(HTTPException) as error:
        product_service.get_products(
            session=session,
            search=None,
            min_price=5000,
            max_price=1000,
            limit=10,
            offset=0,
            sort=ProductSortOption.default,
        )

    assert error.value.status_code == status.HTTP_400_BAD_REQUEST
    assert error.value.detail == "min_price cannot be greater than max_price"


def test_get_products_sort_high_to_low(session):
    product_service.create_product(
        session=session,
        request=create_product_request(
            product_name="Low",
            sku="LOW-001",
            price=1000,
        ),
    )
    product_service.create_product(
        session=session,
        request=create_product_request(
            product_name="High",
            sku="HIGH-001",
            price=5000,
        ),
    )

    result = product_service.get_products(
        session=session,
        search=None,
        min_price=None,
        max_price=None,
        limit=10,
        offset=0,
        sort=ProductSortOption.high_to_low,
    )

    assert result.total == 2
    assert result.items[0].price == 5000
    assert result.items[1].price == 1000


def test_patch_product_success(session):
    created_product = product_service.create_product(
        session=session,
        request=create_product_request(
            product_name="iPhone",
            sku="IPHONE-001",
            price=112000,
            stock_qty=10,
        ),
    )

    patch_request = ProductPatchRequest(price=110000)

    updated_product = product_service.patch_product(
        session=session,
        product_id=created_product.product_id,
        request=patch_request,
    )

    assert updated_product.product_id == created_product.product_id
    assert updated_product.product_name == "iPhone"
    assert updated_product.price == 110000
    assert updated_product.stock_qty == 10


def test_patch_product_empty_body_error(session):
    created_product = product_service.create_product(
        session=session,
        request=create_product_request(
            product_name="iPhone",
            sku="IPHONE-001",
            price=112000,
        ),
    )

    patch_request = ProductPatchRequest()

    with pytest.raises(HTTPException) as error:
        product_service.patch_product(
            session=session,
            product_id=created_product.product_id,
            request=patch_request,
        )

    assert error.value.status_code == status.HTTP_400_BAD_REQUEST
    assert error.value.detail == "At least one field must be provided for update"


def test_delete_product_success(session):
    created_product = product_service.create_product(
        session=session,
        request=create_product_request(
            product_name="iPhone",
            sku="IPHONE-001",
            price=112000,
        ),
    )

    product_service.delete_product(
        session=session,
        product_id=created_product.product_id,
    )

    with pytest.raises(HTTPException) as error:
        product_service.get_product_by_id(
            session=session,
            product_id=created_product.product_id,
        )

    assert error.value.status_code == status.HTTP_404_NOT_FOUND