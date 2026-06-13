from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session

from app.repositories.order_repository import order_repository
from app.repositories.payment_repository import payment_repository
from app.schemas.payment_schema import (
    PaymentCreateRequest,
    PaymentListResponse,
    PaymentMethod,
    PaymentResponse,
    PaymentStatus,
)


class PaymentService:
    def create_payment(
        self,
        session: Session,
        request: PaymentCreateRequest,
    ) -> str:
        order = order_repository.get_by_id(
            session=session,
            order_id=request.order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        paid_payment = payment_repository.get_paid_payment_by_order_id(
            session=session,
            order_id=request.order_id,
        )

        if paid_payment is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This order is already paid",
            )

        payment_method = request.payment_method.value

        if request.payment_method == PaymentMethod.cod:
            payment_status = PaymentStatus.pending.value
            paid_at = None
            transaction_no = None
            message = "Cash on delivery selected successfully"

        else:
            if not request.transaction_no:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction number is required for online payment",
                )

            existing_transaction = payment_repository.get_by_transaction_no(
                session=session,
                transaction_no=request.transaction_no,
            )

            if existing_transaction is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Transaction number already exists",
                )

            payment_status = PaymentStatus.paid.value
            paid_at = datetime.utcnow()
            transaction_no = request.transaction_no
            message = "Payment completed successfully"

        payment_repository.create_payment(
            session=session,
            order_id=order.order_id,
            payment_method=payment_method,
            payment_status=payment_status,
            amount=order.total_amount,
            transaction_no=transaction_no,
            paid_at=paid_at,
        )

        return message

    def get_payments(
        self,
        session: Session,
        order_id: Optional[int],
    ) -> PaymentListResponse:
        total, payments = payment_repository.list_payments(
            session=session,
            order_id=order_id,
        )

        return PaymentListResponse(
            total=total,
            items=[
                PaymentResponse.model_validate(payment)
                for payment in payments
            ],
        )


payment_service = PaymentService()