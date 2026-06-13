from typing import Optional, List

from fastapi import HTTPException, status

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
    def create_product(self, request: ProductCreateRequest) -> ProductResponse:
        return product_repository.create(request)

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = product_repository.get_by_id(product_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    def get_products(
        self,
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

        filtered_products = product_repository.get_all()

        if search:
            normalized_search = search.lower().strip()
            filtered_products = [
                product
                for product in filtered_products
                if normalized_search in product.product_name.lower()
            ]

        if min_price is not None:
            filtered_products = [
                product
                for product in filtered_products
                if product.price >= min_price
            ]

        if max_price is not None:
            filtered_products = [
                product
                for product in filtered_products
                if product.price <= max_price
            ]

        filtered_products = self._sort_products(filtered_products, sort)

        total = len(filtered_products)
        paginated_products = filtered_products[offset: offset + limit]

        return ProductListResponse(
            total=total,
            limit=limit,
            offset=offset,
            items=paginated_products,
        )

    def update_product(
        self,
        product_id: int,
        request: ProductUpdateRequest,
    ) -> ProductResponse:
        self.get_product_by_id(product_id)
        return product_repository.update(product_id, request)

    def patch_product(
        self,
        product_id: int,
        request: ProductPatchRequest,
    ) -> ProductResponse:
        self.get_product_by_id(product_id)

        update_data = request.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided for update",
            )

        return product_repository.patch(product_id, update_data)

    def delete_product(self, product_id: int) -> None:
        self.get_product_by_id(product_id)
        product_repository.delete(product_id)

    def _sort_products(
        self,
        products: List[ProductResponse],
        sort: ProductSortOption,
    ) -> List[ProductResponse]:
        if sort == ProductSortOption.high_to_low:
            return sorted(
                products,
                key=lambda product: product.price,
                reverse=True,
            )

        if sort == ProductSortOption.low_to_high:
            return sorted(
                products,
                key=lambda product: product.price,
            )

        if sort == ProductSortOption.newly_added:
            return sorted(
                products,
                key=lambda product: product.product_id,
                reverse=True,
            )

        return products


product_service = ProductService()