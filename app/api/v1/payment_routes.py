from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.common_schema import MessageResponse
from app.schemas.payment_schema import PaymentCreateRequest, PaymentListResponse
from app.services.payment_service import payment_service

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    request: PaymentCreateRequest,
    session: Session = Depends(get_session),
):
    message = payment_service.create_payment(
        session=session,
        request=request,
    )

    return MessageResponse(
        message=message,
    )


@router.get(
    "",
    response_model=PaymentListResponse,
)
def get_payments(
    order_id: Optional[int] = Query(default=None, gt=0),
    session: Session = Depends(get_session),
):
    return payment_service.get_payments(
        session=session,
        order_id=order_id,
    )