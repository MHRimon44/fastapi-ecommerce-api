from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductListResponse,
    ProductPatchRequest,
    ProductResponse,
    ProductSortOption,
    ProductUpdateRequest,
)
from app.services.product_service import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    request: ProductCreateRequest,
    session: Session = Depends(get_session),
):
    return product_service.create_product(
        session=session,
        request=request,
    )


@router.get(
    "",
    response_model=ProductListResponse,
)
def get_products(
    search: Optional[str] = Query(default=None),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sort: ProductSortOption = Query(default=ProductSortOption.default),
    session: Session = Depends(get_session),
):
    return product_service.get_products(
        session=session,
        search=search,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        offset=offset,
        sort=sort,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product_by_id(
    product_id: int,
    session: Session = Depends(get_session),
):
    return product_service.get_product_by_id(
        session=session,
        product_id=product_id,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    request: ProductUpdateRequest,
    session: Session = Depends(get_session),
):
    return product_service.update_product(
        session=session,
        product_id=product_id,
        request=request,
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def patch_product(
    product_id: int,
    request: ProductPatchRequest,
    session: Session = Depends(get_session),
):
    return product_service.patch_product(
        session=session,
        product_id=product_id,
        request=request,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product_service.delete_product(
        session=session,
        product_id=product_id,
    )

    return None