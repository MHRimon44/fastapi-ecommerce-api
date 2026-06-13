from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.voucher_model import Voucher
from app.schemas.voucher_schema import VoucherCreateRequest


class VoucherRepository:
    def create(
        self,
        session: Session,
        request: VoucherCreateRequest,
    ) -> Voucher:
        voucher = Voucher(
            code=request.code.upper(),
            discount_type=request.discount_type.value,
            discount_value=request.discount_value,
            min_order_amount=request.min_order_amount,
            max_discount_amount=request.max_discount_amount,
            usage_limit=request.usage_limit,
            start_at=request.start_at,
            end_at=request.end_at,
        )

        session.add(voucher)
        session.commit()
        session.refresh(voucher)

        return voucher

    def get_by_code(
        self,
        session: Session,
        code: str,
    ) -> Optional[Voucher]:
        statement = select(Voucher).where(Voucher.code == code.upper())
        return session.exec(statement).first()

    def list_vouchers(
        self,
        session: Session,
    ) -> Tuple[int, List[Voucher]]:
        statement = select(Voucher).order_by(Voucher.created_at.desc())
        count_statement = select(func.count()).select_from(Voucher)

        total = session.exec(count_statement).one()
        vouchers = session.exec(statement).all()

        return total, vouchers


voucher_repository = VoucherRepository()