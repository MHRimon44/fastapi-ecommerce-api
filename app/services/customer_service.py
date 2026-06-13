from fastapi import HTTPException, status
from sqlmodel import Session

from app.repositories.customer_repository import customer_repository
from app.schemas.customer_schema import CustomerCreateRequest, CustomerResponse


class CustomerService:
    def create_customer(
        self,
        session: Session,
        request: CustomerCreateRequest,
    ) -> CustomerResponse:
        customer = customer_repository.create(session, request)
        return CustomerResponse.model_validate(customer)

    def get_customer_by_id(
        self,
        session: Session,
        customer_id: int,
    ) -> CustomerResponse:
        customer = customer_repository.get_by_id(session, customer_id)

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return CustomerResponse.model_validate(customer)


customer_service = CustomerService()