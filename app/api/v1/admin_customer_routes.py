from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_guard import require_admin_user
from app.schemas.admin_customer_schema import (
    AdminCustomerCreateRequest,
    AdminCustomerListResponse,
    AdminCustomerResponse,
    AdminCustomerSingleResponse,
    AdminCustomerUpdateRequest,
)
from app.schemas.common_schema import MessageResponse
from app.services.admin_customer_service import admin_customer_service


router = APIRouter(
    prefix="/admin/customers",
    tags=["Admin Customers"],
    dependencies=[Depends(require_admin_user)],
)


@router.get(
    "",
    response_model=AdminCustomerListResponse,
)
def list_customers(
    search: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    customers, total = admin_customer_service.list_customers(
        session=session,
        search=search,
        page=page,
        page_size=page_size,
    )

    return AdminCustomerListResponse(
        message="Customers retrieved successfully",
        total=total,
        page=page,
        page_size=page_size,
        data=[
            AdminCustomerResponse.model_validate(customer)
            for customer in customers
        ],
    )


@router.get(
    "/{customer_id}",
    response_model=AdminCustomerSingleResponse,
)
def get_customer(
    customer_id: int,
    session: Session = Depends(get_session),
):
    customer = admin_customer_service.get_customer(
        session=session,
        customer_id=customer_id,
    )

    return AdminCustomerSingleResponse(
        message="Customer retrieved successfully",
        data=AdminCustomerResponse.model_validate(customer),
    )


@router.post(
    "",
    response_model=AdminCustomerSingleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    request: AdminCustomerCreateRequest,
    session: Session = Depends(get_session),
):
    customer = admin_customer_service.create_customer(
        session=session,
        request=request,
    )

    return AdminCustomerSingleResponse(
        message="Customer created successfully",
        data=AdminCustomerResponse.model_validate(customer),
    )


@router.put(
    "/{customer_id}",
    response_model=AdminCustomerSingleResponse,
)
def update_customer(
    customer_id: int,
    request: AdminCustomerUpdateRequest,
    session: Session = Depends(get_session),
):
    customer = admin_customer_service.update_customer(
        session=session,
        customer_id=customer_id,
        request=request,
    )

    return AdminCustomerSingleResponse(
        message="Customer updated successfully",
        data=AdminCustomerResponse.model_validate(customer),
    )


@router.delete(
    "/{customer_id}",
    response_model=MessageResponse,
)
def delete_customer(
    customer_id: int,
    session: Session = Depends(get_session),
):
    admin_customer_service.delete_customer(
        session=session,
        customer_id=customer_id,
    )

    return MessageResponse(
        message="Customer deleted successfully",
    )
