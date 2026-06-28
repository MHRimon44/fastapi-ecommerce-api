from typing import List, Optional, Tuple

from sqlalchemy import or_
from sqlmodel import Session, select

from app.models.customer_model import Customer
from app.schemas.admin_customer_schema import (
    AdminCustomerCreateRequest,
    AdminCustomerUpdateRequest,
)


class AdminCustomerRepository:
    def list_customers(
        self,
        session: Session,
        search: Optional[str],
        page: int,
        page_size: int,
    ) -> Tuple[List[Customer], int]:
        statement = select(Customer)

        if search:
            search_pattern = f"%{search}%"
            statement = statement.where(
                or_(
                    Customer.customer_name.ilike(search_pattern),
                    Customer.phone.ilike(search_pattern),
                    Customer.email.ilike(search_pattern),
                )
            )

        all_matching_customers = session.exec(statement).all()
        total = len(all_matching_customers)

        offset = (page - 1) * page_size

        paginated_statement = statement.offset(offset).limit(page_size)
        customers = session.exec(paginated_statement).all()

        return customers, total

    def get_by_id(
        self,
        session: Session,
        customer_id: int,
    ) -> Optional[Customer]:
        statement = select(Customer).where(Customer.customer_id == customer_id)
        return session.exec(statement).first()

    def get_by_phone(
        self,
        session: Session,
        phone: str,
    ) -> Optional[Customer]:
        statement = select(Customer).where(Customer.phone == phone)
        return session.exec(statement).first()

    def get_by_email(
        self,
        session: Session,
        email: str,
    ) -> Optional[Customer]:
        statement = select(Customer).where(Customer.email == email)
        return session.exec(statement).first()

    def create_customer(
        self,
        session: Session,
        request: AdminCustomerCreateRequest,
    ) -> Customer:
        customer = Customer(
            customer_name=request.customer_name,
            phone=request.phone,
            email=request.email,
        )

        session.add(customer)
        session.commit()
        session.refresh(customer)

        return customer

    def update_customer(
        self,
        session: Session,
        customer: Customer,
        request: AdminCustomerUpdateRequest,
    ) -> Customer:
        update_data = request.model_dump(exclude_unset=True)

        for field_name, field_value in update_data.items():
            setattr(customer, field_name, field_value)

        session.add(customer)
        session.commit()
        session.refresh(customer)

        return customer

    def delete_customer(
        self,
        session: Session,
        customer: Customer,
    ) -> None:
        session.delete(customer)
        session.commit()


admin_customer_repository = AdminCustomerRepository()
