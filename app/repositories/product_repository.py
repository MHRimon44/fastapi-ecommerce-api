from typing import Dict, List, Optional

from app.schemas.product_schema import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
)


class InMemoryProductRepository:
    def __init__(self):
        self._products_by_id: Dict[int, ProductResponse] = {}
        self._ordered_product_ids: List[int] = []
        self._next_product_id = 1

    def create(self, request: ProductCreateRequest) -> ProductResponse:
        product = ProductResponse(
            product_id=self._next_product_id,
            product_name=request.product_name,
            price=request.price,
            stock_qty=request.stock_qty,
            description=request.description,
        )

        self._products_by_id[product.product_id] = product
        self._ordered_product_ids.append(product.product_id)
        self._next_product_id += 1

        return product

    def get_all(self) -> List[ProductResponse]:
        return [
            self._products_by_id[product_id]
            for product_id in self._ordered_product_ids
            if product_id in self._products_by_id
        ]

    def get_by_id(self, product_id: int) -> Optional[ProductResponse]:
        return self._products_by_id.get(product_id)

    def update(
        self,
        product_id: int,
        request: ProductUpdateRequest,
    ) -> ProductResponse:
        updated_product = ProductResponse(
            product_id=product_id,
            product_name=request.product_name,
            price=request.price,
            stock_qty=request.stock_qty,
            description=request.description,
        )

        self._products_by_id[product_id] = updated_product

        return updated_product

    def patch(
        self,
        product_id: int,
        update_data: dict,
    ) -> ProductResponse:
        existing_product = self._products_by_id[product_id]
        updated_product = existing_product.model_copy(update=update_data)

        self._products_by_id[product_id] = updated_product

        return updated_product

    def delete(self, product_id: int) -> None:
        self._products_by_id.pop(product_id, None)

        if product_id in self._ordered_product_ids:
            self._ordered_product_ids.remove(product_id)

    def reset(self) -> None:
        self._products_by_id.clear()
        self._ordered_product_ids.clear()
        self._next_product_id = 1
        
product_repository = InMemoryProductRepository()