from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.common_schema import MessageResponse
from app.schemas.voucher_schema import (
    VoucherApplyRequest,
    VoucherCreateRequest,
    VoucherListResponse,
)
from app.services.voucher_service import voucher_service

router = APIRouter(
    prefix="/vouchers",
    tags=["Vouchers"],
)


@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_voucher(
    request: VoucherCreateRequest,
    session: Session = Depends(get_session),
):
    voucher_service.create_voucher(
        session=session,
        request=request,
    )

    return MessageResponse(
        message="Voucher created successfully",
    )


@router.post(
    "/apply",
    response_model=MessageResponse,
)
def apply_voucher(
    request: VoucherApplyRequest,
    session: Session = Depends(get_session),
):
    voucher_service.apply_voucher(
        session=session,
        order_id=request.order_id,
        voucher_code=request.voucher_code,
    )

    return MessageResponse(
        message="Voucher applied successfully",
    )


@router.get(
    "",
    response_model=VoucherListResponse,
)
def get_vouchers(
    session: Session = Depends(get_session),
):
    return voucher_service.get_vouchers(
        session=session,
    )