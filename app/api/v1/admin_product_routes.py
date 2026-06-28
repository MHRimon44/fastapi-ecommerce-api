from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_guard import require_admin_user
from app.schemas.admin_product_schema import (
    AdminProductCreateRequest,
    AdminProductListResponse,
    AdminProductResponse,
    AdminProductSingleResponse,
    AdminProductStatusUpdateRequest,
    AdminProductStockUpdateRequest,
    AdminProductUpdateRequest,
)
from app.schemas.common_schema import MessageResponse
from app.services.admin_product_service import admin_product_service


router = APIRouter(
    prefix="/admin/products",
    tags=["Admin Products"],
    dependencies=[Depends(require_admin_user)],
)


@router.get(
    "",
    response_model=AdminProductListResponse,
)
def list_products(
    search: Optional[str] = Query(default=None),
    is_active: Optional[bool] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    products, total = admin_product_service.list_products(
        session=session,
        search=search,
        is_active=is_active,
        page=page,
        page_size=page_size,
    )

    return AdminProductListResponse(
        message="Products retrieved successfully",
        total=total,
        page=page,
        page_size=page_size,
        data=[
            AdminProductResponse.model_validate(product)
            for product in products
        ],
    )


@router.get(
    "/{product_id}",
    response_model=AdminProductSingleResponse,
)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = admin_product_service.get_product(
        session=session,
        product_id=product_id,
    )

    return AdminProductSingleResponse(
        message="Product retrieved successfully",
        data=AdminProductResponse.model_validate(product),
    )


@router.post(
    "",
    response_model=AdminProductSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    request: AdminProductCreateRequest,
    session: Session = Depends(get_session),
):
    product = admin_product_service.create_product(
        session=session,
        request=request,
    )

    return AdminProductSingleResponse(
        message="Product created successfully",
        data=AdminProductResponse.model_validate(product),
    )


@router.put(
    "/{product_id}",
    response_model=AdminProductSingleResponse,
)
def update_product(
    product_id: int,
    request: AdminProductUpdateRequest,
    session: Session = Depends(get_session),
):
    product = admin_product_service.update_product(
        session=session,
        product_id=product_id,
        request=request,
    )

    return AdminProductSingleResponse(
        message="Product updated successfully",
        data=AdminProductResponse.model_validate(product),
    )


@router.patch(
    "/{product_id}/stock",
    response_model=AdminProductSingleResponse,
)
def update_product_stock(
    product_id: int,
    request: AdminProductStockUpdateRequest,
    session: Session = Depends(get_session),
):
    product = admin_product_service.update_stock(
        session=session,
        product_id=product_id,
        request=request,
    )

    return AdminProductSingleResponse(
        message="Product stock updated successfully",
        data=AdminProductResponse.model_validate(product),
    )


@router.patch(
    "/{product_id}/status",
    response_model=AdminProductSingleResponse,
)
def update_product_status(
    product_id: int,
    request: AdminProductStatusUpdateRequest,
    session: Session = Depends(get_session),
):
    product = admin_product_service.update_status(
        session=session,
        product_id=product_id,
        request=request,
    )

    return AdminProductSingleResponse(
        message="Product status updated successfully",
        data=AdminProductResponse.model_validate(product),
    )


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    admin_product_service.delete_product(
        session=session,
        product_id=product_id,
    )

    return MessageResponse(
        message="Product deleted successfully",
    )
