from typing import Dict, List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.repositories.customer_repository import customer_repository
from app.repositories.order_repository import order_repository
from app.repositories.product_repository import product_repository
from app.schemas.order_schema import (
    OrderCreateRequest,
    OrderItemResponse,
    OrderListResponse,
    OrderResponse,
    OrderStatus,
    OrderSummaryResponse,
)


class OrderService:
    def create_order(
        self,
        session: Session,
        request: OrderCreateRequest,
    ) -> OrderResponse:
        try:
            customer = customer_repository.get_by_id(
                session=session,
                customer_id=request.customer_id,
            )

            if customer is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found",
                )

            order_items_data: List[Dict] = []

            for request_item in request.items:
                product = product_repository.get_by_id(
                    session=session,
                    product_id=request_item.product_id,
                )

                if product is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Product {request_item.product_id} not found",
                    )

                if product.stock_qty < request_item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for product {product.product_name}",
                    )

                unit_price = product.price
                line_total = unit_price * request_item.quantity

                product.stock_qty -= request_item.quantity
                session.add(product)

                order_items_data.append(
                    {
                        "product_id": product.product_id,
                        "quantity": request_item.quantity,
                        "unit_price": unit_price,
                        "line_total": line_total,
                    }
                )

            order, order_items = order_repository.create_order(
                session=session,
                customer_id=customer.customer_id,
                order_items_data=order_items_data,
            )

            return OrderResponse(
                order_id=order.order_id,
                order_no=order.order_no,
                customer_id=order.customer_id,
                order_status=order.order_status,
                total_amount=order.total_amount,
                created_at=order.created_at,
                items=[
                    OrderItemResponse.model_validate(item)
                    for item in order_items
                ],
            )

        except HTTPException:
            session.rollback()
            raise

        except Exception:
            session.rollback()
            raise

    def get_order_by_id(
        self,
        session: Session,
        order_id: int,
    ) -> OrderResponse:
        order = order_repository.get_by_id(
            session=session,
            order_id=order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        return OrderResponse(
            order_id=order.order_id,
            order_no=order.order_no,
            customer_id=order.customer_id,
            order_status=order.order_status,
            total_amount=order.total_amount,
            created_at=order.created_at,
            items=[
                OrderItemResponse.model_validate(item)
                for item in order.items
            ],
        )

    def get_orders(
        self,
        session: Session,
        customer_id: Optional[int],
        order_status: Optional[OrderStatus],
        limit: int,
        offset: int,
    ) -> OrderListResponse:
        if customer_id is not None:
            customer = customer_repository.get_by_id(
                session=session,
                customer_id=customer_id,
            )

            if customer is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Customer not found",
                )
        status_value = order_status.value if order_status else None

        total, orders = order_repository.list_orders(
            session=session,
            customer_id=customer_id,
            status=status_value,
            limit=limit,
            offset=offset,
        )

        return OrderListResponse(
            total=total,
            limit=limit,
            offset=offset,
            items=[
                OrderSummaryResponse.model_validate(order)
                for order in orders
            ],
        )


order_service = OrderService()