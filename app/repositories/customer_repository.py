from typing import List, Optional

from sqlmodel import Session, select

from app.models.customer_model import Customer
from app.schemas.customer_schema import CustomerCreateRequest


class CustomerRepository:
    def create(
        self,
        session: Session,
        request: CustomerCreateRequest,
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

    def get_by_id(
        self,
        session: Session,
        customer_id: int,
    ) -> Optional[Customer]:
        return session.get(Customer, customer_id)

    def list_customers(
        self,
        session: Session,
    ) -> List[Customer]:
        statement = select(Customer).order_by(Customer.customer_id.desc())
        return session.exec(statement).all()


customer_repository = CustomerRepository()