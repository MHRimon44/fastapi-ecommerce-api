from typing import List, Optional, Tuple

from sqlalchemy import or_
from sqlmodel import Session, select

from app.models.product_model import Product
from app.schemas.admin_product_schema import (
    AdminProductCreateRequest,
    AdminProductUpdateRequest,
)


class AdminProductRepository:
    def list_products(
        self,
        session: Session,
        search: Optional[str],
        is_active: Optional[bool],
        page: int,
        page_size: int,
    ) -> Tuple[List[Product], int]:
        statement = select(Product)

        if search:
            search_pattern = f"%{search}%"
            statement = statement.where(
                or_(
                    Product.product_name.ilike(search_pattern),
                    Product.sku.ilike(search_pattern),
                )
            )

        if is_active is not None:
            statement = statement.where(Product.is_active == is_active)

        all_matching_products = session.exec(statement).all()
        total = len(all_matching_products)

        offset = (page - 1) * page_size

        paginated_statement = statement.offset(offset).limit(page_size)
        products = session.exec(paginated_statement).all()

        return products, total

    def get_by_id(
        self,
        session: Session,
        product_id: int,
    ) -> Optional[Product]:
        statement = select(Product).where(Product.product_id == product_id)
        return session.exec(statement).first()

    def get_by_sku(
        self,
        session: Session,
        sku: str,
    ) -> Optional[Product]:
        statement = select(Product).where(Product.sku == sku)
        return session.exec(statement).first()

    def create_product(
        self,
        session: Session,
        request: AdminProductCreateRequest,
    ) -> Product:
        product = Product(
            product_name=request.product_name,
            sku=request.sku,
            price=request.price,
            stock_qty=request.stock_qty,
            description=request.description,
            is_active=request.is_active,
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def update_product(
        self,
        session: Session,
        product: Product,
        request: AdminProductUpdateRequest,
    ) -> Product:
        update_data = request.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(product, field_name, field_value)

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def update_stock(
        self,
        session: Session,
        product: Product,
        stock_qty: int,
    ) -> Product:
        product.stock_qty = stock_qty

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def update_status(
        self,
        session: Session,
        product: Product,
        is_active: bool,
    ) -> Product:
        product.is_active = is_active

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def delete_product(
        self,
        session: Session,
        product: Product,
    ) -> None:
        session.delete(product)
        session.commit()


admin_product_repository = AdminProductRepository()
