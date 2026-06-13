from typing import Optional

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.product_model import Product
from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductPatchRequest,
    ProductSortOption,
    ProductUpdateRequest,
)


class ProductRepository:
    def create(
        self,
        session: Session,
        request: ProductCreateRequest,
    ) -> Product:
        product = Product(
            product_name=request.product_name,
            sku=request.sku,
            price=request.price,
            stock_qty=request.stock_qty,
            description=request.description,
        )

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def get_by_id(
        self,
        session: Session,
        product_id: int,
    ) -> Optional[Product]:
        return session.get(Product, product_id)

    def list_products(
        self,
        session: Session,
        search: Optional[str],
        min_price: Optional[float],
        max_price: Optional[float],
        limit: int,
        offset: int,
        sort: ProductSortOption,
    ):
        statement = select(Product)
        count_statement = select(func.count()).select_from(Product)

        if search:
            normalized_search = search.lower().strip()
            statement = statement.where(
                func.lower(Product.product_name).like(f"%{normalized_search}%")
            )
            count_statement = count_statement.where(
                func.lower(Product.product_name).like(f"%{normalized_search}%")
            )

        if min_price is not None:
            statement = statement.where(Product.price >= min_price)
            count_statement = count_statement.where(Product.price >= min_price)

        if max_price is not None:
            statement = statement.where(Product.price <= max_price)
            count_statement = count_statement.where(Product.price <= max_price)

        if sort == ProductSortOption.high_to_low:
            statement = statement.order_by(Product.price.desc())

        elif sort == ProductSortOption.low_to_high:
            statement = statement.order_by(Product.price.asc())

        elif sort == ProductSortOption.newly_added:
            statement = statement.order_by(Product.product_id.desc())

        else:
            statement = statement.order_by(Product.product_id.asc())

        total = session.exec(count_statement).one()

        statement = statement.offset(offset).limit(limit)

        items = session.exec(statement).all()

        return total, items

    def update(
        self,
        session: Session,
        product: Product,
        request: ProductUpdateRequest,
    ) -> Product:
        product.product_name = request.product_name
        product.sku = request.sku
        product.price = request.price
        product.stock_qty = request.stock_qty
        product.description = request.description

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def patch(
        self,
        session: Session,
        product: Product,
        request: ProductPatchRequest,
    ) -> Product:
        update_data = request.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(product, field_name, field_value)

        session.add(product)
        session.commit()
        session.refresh(product)

        return product

    def delete(
        self,
        session: Session,
        product: Product,
    ) -> None:
        session.delete(product)
        session.commit()


product_repository = ProductRepository()