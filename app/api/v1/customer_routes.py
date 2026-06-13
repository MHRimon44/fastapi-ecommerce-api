from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.customer_schema import (
    CustomerCreateRequest,
    CustomerResponse,
)
from app.services.customer_service import customer_service
from app.schemas.common_schema import MessageResponse

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    request: CustomerCreateRequest,
    session: Session = Depends(get_session),
):
    customer_service.create_customer(
        session=session,
        request=request,
    )

    return MessageResponse(
        message="Customer created successfully",
    )
@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer_by_id(
    customer_id: int,
    session: Session = Depends(get_session),
):
    return customer_service.get_customer_by_id(
        session=session,
        customer_id=customer_id,
    )