from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_guard import require_admin_user
from app.schemas.admin_report_schema import (
    DashboardReportResponse,
    ProductPerformanceResponse,
    SalesSummaryResponse,
    VoucherUsageResponse,
)
from app.services.admin_report_service import admin_report_service


router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"],
    dependencies=[Depends(require_admin_user)],
)


@router.get(
    "/dashboard",
    response_model=DashboardReportResponse,
    status_code=status.HTTP_200_OK,
)
def get_dashboard_report(
    session: Session = Depends(get_session),
) -> DashboardReportResponse:
    data = admin_report_service.get_dashboard_report(session)

    return DashboardReportResponse(
        message="Dashboard report retrieved successfully",
        data=data,
    )


@router.get(
    "/sales-summary",
    response_model=SalesSummaryResponse,
    status_code=status.HTTP_200_OK,
)
def get_sales_summary(
    session: Session = Depends(get_session),
) -> SalesSummaryResponse:
    data = admin_report_service.get_sales_summary(session)

    return SalesSummaryResponse(
        message="Sales summary report retrieved successfully",
        data=data,
    )


@router.get(
    "/product-performance",
    response_model=ProductPerformanceResponse,
    status_code=status.HTTP_200_OK,
)
def get_product_performance(
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
) -> ProductPerformanceResponse:
    data = admin_report_service.get_product_performance(
        session=session,
        limit=limit,
    )

    return ProductPerformanceResponse(
        message="Product performance report retrieved successfully",
        data=data,
    )


@router.get(
    "/voucher-usage",
    response_model=VoucherUsageResponse,
    status_code=status.HTTP_200_OK,
)
def get_voucher_usage(
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
) -> VoucherUsageResponse:
    data = admin_report_service.get_voucher_usage(
        session=session,
        limit=limit,
    )

    return VoucherUsageResponse(
        message="Voucher usage report retrieved successfully",
        data=data,
    )
