from typing import Dict, List, Optional, Tuple

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.order_model import Order
from app.repositories.admin_order_repository import admin_order_repository
from app.schemas.admin_order_schema import (
    AdminOrderCustomerResponse,
    AdminOrderDetailResponseData,
    AdminOrderItemResponse,
    AdminOrderResponse,
)


ALLOWED_ORDER_STATUSES = [
    "Pending",
    "Confirmed",
    "Processing",
    "Shipped",
    "Delivered",
    "Cancelled",
]


class AdminOrderService:
    def list_orders(
        self,
        session: Session,
        search: Optional[str],
        order_status_filter: Optional[str],
        customer_id: Optional[int],
        page: int,
        page_size: int,
    ) -> Tuple[List[Order], int]:
        if order_status_filter and order_status_filter not in ALLOWED_ORDER_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status filter",
            )

        return admin_order_repository.list_orders(
            session=session,
            search=search,
            order_status_filter=order_status_filter,
            customer_id=customer_id,
            page=page,
            page_size=page_size,
        )

    def get_order(
        self,
        session: Session,
        order_id: int,
    ) -> Order:
        order = admin_order_repository.get_order_by_id(
            session=session,
            order_id=order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return order

    def get_order_detail(
        self,
        session: Session,
        order_id: int,
    ) -> AdminOrderDetailResponseData:
        order = self.get_order(
            session=session,
            order_id=order_id,
        )

        customer = admin_order_repository.get_customer_by_id(
            session=session,
            customer_id=order.customer_id,
        )

        order_items = admin_order_repository.list_order_items(
            session=session,
            order_id=order_id,
        )

        product_ids = list({item.product_id for item in order_items})

        products = admin_order_repository.get_products_by_ids(
            session=session,
            product_ids=product_ids,
        )

        product_name_map: Dict[int, str] = {
            product.product_id: product.product_name
            for product in products
        }

        return AdminOrderDetailResponseData(
            order=AdminOrderResponse.model_validate(order),
            customer=(
                AdminOrderCustomerResponse.model_validate(customer)
                if customer is not None
                else None
            ),
            items=[
                AdminOrderItemResponse(
                    order_item_id=item.order_item_id,
                    order_id=item.order_id,
                    product_id=item.product_id,
                    product_name=product_name_map.get(item.product_id),
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    line_total=item.line_total,
                )
                for item in order_items
            ],
        )

    def get_order_items(
        self,
        session: Session,
        order_id: int,
    ) -> List[AdminOrderItemResponse]:
        self.get_order(
            session=session,
            order_id=order_id,
        )

        order_items = admin_order_repository.list_order_items(
            session=session,
            order_id=order_id,
        )

        product_ids = list({item.product_id for item in order_items})

        products = admin_order_repository.get_products_by_ids(
            session=session,
            product_ids=product_ids,
        )

        product_name_map: Dict[int, str] = {
            product.product_id: product.product_name
            for product in products
        }

        return [
            AdminOrderItemResponse(
                order_item_id=item.order_item_id,
                order_id=item.order_id,
                product_id=item.product_id,
                product_name=product_name_map.get(item.product_id),
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=item.line_total,
            )
            for item in order_items
        ]

    def update_order_status(
        self,
        session: Session,
        order_id: int,
        new_status: str,
    ) -> Order:
        if new_status not in ALLOWED_ORDER_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status",
            )

        order = self.get_order(
            session=session,
            order_id=order_id,
        )

        if order.order_status == "Cancelled" and new_status != "Cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled order status cannot be changed",
            )

        if order.order_status == "Delivered" and new_status != "Delivered":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivered order status cannot be changed",
            )

        return admin_order_repository.update_order_status(
            session=session,
            order=order,
            order_status=new_status,
        )

    def cancel_order(
        self,
        session: Session,
        order_id: int,
    ) -> Order:
        order = self.get_order(
            session=session,
            order_id=order_id,
        )

        if order.order_status == "Delivered":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivered order cannot be cancelled",
            )

        if order.order_status == "Cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order already cancelled",
            )

        return admin_order_repository.update_order_status(
            session=session,
            order=order,
            order_status="Cancelled",
        )


admin_order_service = AdminOrderService()
