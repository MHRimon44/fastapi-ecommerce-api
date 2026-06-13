from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.order_schema import (
    OrderCreateRequest,
    OrderCreateResponse,
    OrderResponse,
)
from app.services.order_service import order_service
from app.schemas.common_schema import OrderPlacedResponse

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