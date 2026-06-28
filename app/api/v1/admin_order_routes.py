from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_guard import require_admin_user
from app.schemas.admin_order_schema import (
    AdminOrderItemsResponse,
    AdminOrderListResponse,
    AdminOrderResponse,
    AdminOrderSingleResponse,
    AdminOrderStatusUpdateRequest,
)
from app.services.admin_order_service import admin_order_service


router = APIRouter(
    prefix="/admin/orders",
    tags=["Admin Orders"],
    dependencies=[Depends(require_admin_user)],
)


@router.get(
    "",
    response_model=AdminOrderListResponse,
)
def list_orders(
    search: Optional[str] = Query(default=None),
    order_status: Optional[str] = Query(default=None),
    customer_id: Optional[int] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    orders, total = admin_order_service.list_orders(
        session=session,
        search=search,
        order_status_filter=order_status,
        customer_id=customer_id,
        page=page,
        page_size=page_size,
    )

    return AdminOrderListResponse(
        message="Orders retrieved successfully",
        total=total,
        page=page,
        page_size=page_size,
        data=[
            AdminOrderResponse.model_validate(order)
            for order in orders
        ],
    )


@router.get(
    "/{order_id}",
    response_model=AdminOrderSingleResponse,
)
def get_order(
    order_id: int,
    session: Session = Depends(get_session),
):
    order_detail = admin_order_service.get_order_detail(
        session=session,
        order_id=order_id,
    )

    return AdminOrderSingleResponse(
        message="Order retrieved successfully",
        data=order_detail,
    )


@router.get(
    "/{order_id}/items",
    response_model=AdminOrderItemsResponse,
)
def get_order_items(
    order_id: int,
    session: Session = Depends(get_session),
):
    items = admin_order_service.get_order_items(
        session=session,
        order_id=order_id,
    )

    return AdminOrderItemsResponse(
        message="Order items retrieved successfully",
        total=len(items),
        data=items,
    )


@router.patch(
    "/{order_id}/status",
    response_model=AdminOrderSingleResponse,
)
def update_order_status(
    order_id: int,
    request: AdminOrderStatusUpdateRequest,
    session: Session = Depends(get_session),
):
    admin_order_service.update_order_status(
        session=session,
        order_id=order_id,
        new_status=request.order_status,
    )

    order_detail = admin_order_service.get_order_detail(
        session=session,
        order_id=order_id,
    )

    return AdminOrderSingleResponse(
        message="Order status updated successfully",
        data=order_detail,
    )


@router.patch(
    "/{order_id}/cancel",
    response_model=AdminOrderSingleResponse,
)
def cancel_order(
    order_id: int,
    session: Session = Depends(get_session),
):
    admin_order_service.cancel_order(
        session=session,
        order_id=order_id,
    )

    order_detail = admin_order_service.get_order_detail(
        session=session,
        order_id=order_id,
    )

    return AdminOrderSingleResponse(
        message="Order cancelled successfully",
        data=order_detail,
    )
