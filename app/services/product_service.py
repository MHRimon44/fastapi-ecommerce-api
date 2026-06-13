from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.repositories.product_repository import product_repository
from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductListResponse,
    ProductPatchRequest,
    ProductResponse,
    ProductSortOption,
    ProductUpdateRequest,
)


class ProductService:
    def create_product(
        self,
        session: Session,
        request: ProductCreateRequest,
    ) -> ProductResponse:
        product = product_repository.create(session, request)
        return ProductResponse.model_validate(product)

    def get_product_by_id(
        self,
        session: Session,
        product_id: int,
    ) -> ProductResponse:
        product = self._get_product_or_404(session, product_id)
        return ProductResponse.model_validate(product)

    def get_products(
        self,
        session: Session,
        search: Optional[str],
        min_price: Optional[float],
        max_price: Optional[float],
        limit: int,
        offset: int,
        sort: ProductSortOption,
    ) -> ProductListResponse:
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_price cannot be greater than max_price",
            )

        total, items = product_repository.list_products(
            session=session,
            search=search,
            min_price=min_price,
            max_price=max_price,
            limit=limit,
            offset=offset,
            sort=sort,
        )

        return ProductListResponse(
            total=total,
            limit=limit,
            offset=offset,
            items=[
                ProductResponse.model_validate(product)
                for product in items
            ],
        )

    def update_product(
        self,
        session: Session,
        product_id: int,
        request: ProductUpdateRequest,
    ) -> ProductResponse:
        product = self._get_product_or_404(session, product_id)

        updated_product = product_repository.update(
            session=session,
            product=product,
            request=request,
        )

        return ProductResponse.model_validate(updated_product)

    def patch_product(
        self,
        session: Session,
        product_id: int,
        request: ProductPatchRequest,
    ) -> ProductResponse:
        product = self._get_product_or_404(session, product_id)

        update_data = request.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update",
            )

        updated_product = product_repository.patch(
            session=session,
            product=product,
            request=request,
        )

        return ProductResponse.model_validate(updated_product)

    def delete_product(
        self,
        session: Session,
        product_id: int,
    ) -> None:
        product = self._get_product_or_404(session, product_id)

        product_repository.delete(
            session=session,
            product=product,
        )

    def _get_product_or_404(
        self,
        session: Session,
        product_id: int,
    ):
        product = product_repository.get_by_id(session, product_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product


product_service = ProductService()