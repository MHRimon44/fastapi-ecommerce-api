from datetime import datetime

from fastapi import HTTPException, status
from sqlmodel import Session

from app.repositories.order_repository import order_repository
from app.repositories.voucher_repository import voucher_repository
from app.schemas.voucher_schema import (
    DiscountType,
    VoucherCreateRequest,
    VoucherListResponse,
    VoucherResponse,
)


class VoucherService:
    def create_voucher(
        self,
        session: Session,
        request: VoucherCreateRequest,
    ) -> None:
        existing_voucher = voucher_repository.get_by_code(
            session=session,
            code=request.code,
        )

        if existing_voucher is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher code already exists",
            )

        if request.discount_type == DiscountType.percentage and request.discount_value > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Percentage discount cannot be greater than 100",
            )

        if request.start_at and request.end_at and request.start_at >= request.end_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher start date must be before end date",
            )

        voucher_repository.create(
            session=session,
            request=request,
        )

    def apply_voucher(
        self,
        session: Session,
        order_id: int,
        voucher_code: str,
    ) -> None:
        order = order_repository.get_by_id(
            session=session,
            order_id=order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        if order.voucher_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher already applied to this order",
            )

        voucher = voucher_repository.get_by_code(
            session=session,
            code=voucher_code,
        )

        if voucher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Voucher not found",
            )

        if not voucher.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher is not active",
            )

        now = datetime.utcnow()

        if voucher.start_at and now < voucher.start_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher is not started yet",
            )

        if voucher.end_at and now > voucher.end_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher has expired",
            )

        if voucher.usage_limit is not None and voucher.used_count >= voucher.usage_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher usage limit exceeded",
            )

        sub_total = order.sub_total if order.sub_total > 0 else order.total_amount

        if sub_total < voucher.min_order_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order amount is lower than voucher minimum purchase amount",
            )

        if voucher.discount_type == DiscountType.flat.value:
            discount_amount = voucher.discount_value
        else:
            discount_amount = sub_total * voucher.discount_value / 100

            if voucher.max_discount_amount is not None:
                discount_amount = min(discount_amount, voucher.max_discount_amount)

        discount_amount = min(discount_amount, sub_total)
        payable_amount = sub_total - discount_amount

        order.sub_total = sub_total
        order.discount_amount = discount_amount
        order.total_amount = payable_amount
        order.voucher_code = voucher.code

        voucher.used_count += 1

        session.add(order)
        session.add(voucher)
        session.commit()

    def get_vouchers(
        self,
        session: Session,
    ) -> VoucherListResponse:
        total, vouchers = voucher_repository.list_vouchers(session=session)

        return VoucherListResponse(
            total=total,
            items=[
                VoucherResponse.model_validate(voucher)
                for voucher in vouchers
            ],
        )


voucher_service = VoucherService()