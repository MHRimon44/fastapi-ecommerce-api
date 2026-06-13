from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.common_schema import OrderPlacedResponse
from app.schemas.order_schema import (
    OrderCreateRequest,
    OrderListResponse,
    OrderResponse,
    OrderStatus,
)
from app.services.order_service import order_service

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderPlacedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    request: OrderCreateRequest,
    session: Session = Depends(get_session),
):
    order = order_service.create_order(
        session=session,
        request=request,
    )

    return OrderPlacedResponse(
        message="Order placed successfully",
        order_no=order.order_no,
    )


@router.get(
    "",
    response_model=OrderListResponse,
)
def get_orders(
    customer_id: Optional[int] = Query(default=None, gt=0),
    order_status: Optional[OrderStatus] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_session),
):
    return order_service.get_orders(
        session=session,
        customer_id=customer_id,
        order_status=order_status,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order_by_id(
    order_id: int,
    session: Session = Depends(get_session),
):
    return order_service.get_order_by_id(
        session=session,
        order_id=order_id,
    )