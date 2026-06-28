from typing import List, Optional, Tuple

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.customer_model import Customer
from app.repositories.admin_customer_repository import admin_customer_repository
from app.schemas.admin_customer_schema import (
    AdminCustomerCreateRequest,
    AdminCustomerUpdateRequest,
)


class AdminCustomerService:
    def list_customers(
        self,
        session: Session,
        search: Optional[str],
        page: int,
        page_size: int,
    ) -> Tuple[List[Customer], int]:
        return admin_customer_repository.list_customers(
            session=session,
            search=search,
            page=page,
            page_size=page_size,
        )

    def get_customer(
        self,
        session: Session,
        customer_id: int,
    ) -> Customer:
        customer = admin_customer_repository.get_by_id(
            session=session,
            customer_id=customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return customer

    def create_customer(
        self,
        session: Session,
        request: AdminCustomerCreateRequest,
    ) -> Customer:
        existing_phone_customer = admin_customer_repository.get_by_phone(
            session=session,
            phone=request.phone,
        )

        if existing_phone_customer is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer phone already exists",
            )

        if request.email:
            existing_email_customer = admin_customer_repository.get_by_email(
                session=session,
                email=request.email,
            )

            if existing_email_customer is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Customer email already exists",
                )

        return admin_customer_repository.create_customer(
            session=session,
            request=request,
        )

    def update_customer(
        self,
        session: Session,
        customer_id: int,
        request: AdminCustomerUpdateRequest,
    ) -> Customer:
        customer = self.get_customer(
            session=session,
            customer_id=customer_id,
        )

        if request.phone:
            existing_phone_customer = admin_customer_repository.get_by_phone(
                session=session,
                phone=request.phone,
            )

            if (
                existing_phone_customer is not None
                and existing_phone_customer.customer_id != customer_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Customer phone already exists",
                )

        if request.email:
            existing_email_customer = admin_customer_repository.get_by_email(
                session=session,
                email=request.email,
            )

            if (
                existing_email_customer is not None
                and existing_email_customer.customer_id != customer_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Customer email already exists",
                )

        return admin_customer_repository.update_customer(
            session=session,
            customer=customer,
            request=request,
        )

    def delete_customer(
        self,
        session: Session,
        customer_id: int,
    ) -> None:
        customer = self.get_customer(
            session=session,
            customer_id=customer_id,
        )

        try:
            admin_customer_repository.delete_customer(
                session=session,
                customer=customer,
            )
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer cannot be deleted because customer has related orders",
            )


admin_customer_service = AdminCustomerService()
