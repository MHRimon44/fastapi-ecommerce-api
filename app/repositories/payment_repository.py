from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.payment_model import Payment


class PaymentRepository:
    def create_payment(
        self,
        session: Session,
        order_id: int,
        payment_method: str,
        payment_status: str,
        amount: float,
        transaction_no: Optional[str],
        paid_at: Optional[datetime],
    ) -> Payment:
        payment = Payment(
            order_id=order_id,
            payment_method=payment_method,
            payment_status=payment_status,
            amount=amount,
            transaction_no=transaction_no,
            paid_at=paid_at,
        )

        session.add(payment)
        session.commit()
        session.refresh(payment)

        return payment

    def get_paid_payment_by_order_id(
        self,
        session: Session,
        order_id: int,
    ) -> Optional[Payment]:
        statement = select(Payment).where(
            Payment.order_id == order_id,
            Payment.payment_status == "PAID",
        )

        return session.exec(statement).first()

    def get_by_transaction_no(
        self,
        session: Session,
        transaction_no: str,
    ) -> Optional[Payment]:
        statement = select(Payment).where(
            Payment.transaction_no == transaction_no,
        )

        return session.exec(statement).first()

    def list_payments(
        self,
        session: Session,
        order_id: Optional[int],
    ) -> Tuple[int, List[Payment]]:
        statement = select(Payment)
        count_statement = select(func.count()).select_from(Payment)

        if order_id is not None:
            statement = statement.where(Payment.order_id == order_id)
            count_statement = count_statement.where(Payment.order_id == order_id)

        statement = statement.order_by(Payment.created_at.desc())

        total = session.exec(count_statement).one()
        payments = session.exec(statement).all()

        return total, payments


payment_repository = PaymentRepository()