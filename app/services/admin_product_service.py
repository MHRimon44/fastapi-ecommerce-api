from typing import Optional, Tuple, List

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.product_model import Product
from app.repositories.admin_product_repository import admin_product_repository
from app.schemas.admin_product_schema import (
    AdminProductCreateRequest,
    AdminProductStatusUpdateRequest,
    AdminProductStockUpdateRequest,
    AdminProductUpdateRequest,
)


class AdminProductService:
    def list_products(
        self,
        session: Session,
        search: Optional[str],
        is_active: Optional[bool],
        page: int,
        page_size: int,
    ) -> Tuple[List[Product], int]:
        return admin_product_repository.list_products(
            session=session,
            search=search,
            is_active=is_active,
            page=page,
            page_size=page_size,
        )

    def get_product(
        self,
        session: Session,
        product_id: int,
    ) -> Product:
        product = admin_product_repository.get_by_id(
            session=session,
            product_id=product_id,
        )

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    def create_product(
        self,
        session: Session,
        request: AdminProductCreateRequest,
    ) -> Product:
        if request.sku:
            existing_product = admin_product_repository.get_by_sku(
                session=session,
                sku=request.sku,
            )

            if existing_product is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product SKU already exists",
                )

        return admin_product_repository.create_product(
            session=session,
            request=request,
        )

    def update_product(
        self,
        session: Session,
        product_id: int,
        request: AdminProductUpdateRequest,
    ) -> Product:
        product = self.get_product(
            session=session,
            product_id=product_id,
        )

        if request.sku:
            existing_product = admin_product_repository.get_by_sku(
                session=session,
                sku=request.sku,
            )

            if existing_product is not None and existing_product.product_id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product SKU already exists",
                )

        return admin_product_repository.update_product(
            session=session,
            product=product,
            request=request,
        )

    def update_stock(
        self,
        session: Session,
        product_id: int,
        request: AdminProductStockUpdateRequest,
    ) -> Product:
        product = self.get_product(
            session=session,
            product_id=product_id,
        )

        return admin_product_repository.update_stock(
            session=session,
            product=product,
            stock_qty=request.stock_qty,
        )

    def update_status(
        self,
        session: Session,
        product_id: int,
        request: AdminProductStatusUpdateRequest,
    ) -> Product:
        product = self.get_product(
            session=session,
            product_id=product_id,
        )

        return admin_product_repository.update_status(
            session=session,
            product=product,
            is_active=request.is_active,
        )

    def delete_product(
        self,
        session: Session,
        product_id: int,
    ) -> None:
        product = self.get_product(
            session=session,
            product_id=product_id,
        )

        admin_product_repository.delete_product(
            session=session,
            product=product,
        )


admin_product_service = AdminProductService()
