from typing import List

from sqlmodel import Session

from app.repositories.admin_report_repository import admin_report_repository
from app.schemas.admin_report_schema import (
    DashboardReportData,
    OrderStatusSummary,
    PaymentMethodSummary,
    ProductPerformanceItem,
    SalesSummaryData,
    VoucherUsageItem,
)


class AdminReportService:
    def get_dashboard_report(
        self,
        session: Session,
    ) -> DashboardReportData:
        data = admin_report_repository.get_dashboard_report(session)

        return DashboardReportData(**data)

    def get_sales_summary(
        self,
        session: Session,
    ) -> SalesSummaryData:
        result = admin_report_repository.get_sales_summary(session)

        summary = result["summary"]

        return SalesSummaryData(
            total_orders=int(summary.get("total_orders") or 0),
            total_sales_amount=float(summary.get("total_sales_amount") or 0),
            total_discount_amount=float(summary.get("total_discount_amount") or 0),
            average_order_value=float(summary.get("average_order_value") or 0),
            by_status=[
                OrderStatusSummary(
                    order_status=str(row.get("order_status")),
                    total_orders=int(row.get("total_orders") or 0),
                    total_amount=float(row.get("total_amount") or 0),
                )
                for row in result["by_status"]
            ],
            by_payment_method=[
                PaymentMethodSummary(
                    payment_method=str(row.get("payment_method")),
                    total_payments=int(row.get("total_payments") or 0),
                    total_amount=float(row.get("total_amount") or 0),
                )
                for row in result["by_payment_method"]
            ],
        )

    def get_product_performance(
        self,
        session: Session,
        limit: int,
    ) -> List[ProductPerformanceItem]:
        rows = admin_report_repository.get_product_performance(
            session=session,
            limit=limit,
        )

        return [
            ProductPerformanceItem(
                product_id=int(row.get("product_id")),
                product_name=str(row.get("product_name")),
                sku=row.get("sku"),
                price=float(row.get("price") or 0),
                current_stock_qty=int(row.get("current_stock_qty") or 0),
                quantity_sold=int(row.get("quantity_sold") or 0),
                sales_amount=float(row.get("sales_amount") or 0),
            )
            for row in rows
        ]

    def get_voucher_usage(
        self,
        session: Session,
        limit: int,
    ) -> List[VoucherUsageItem]:
        rows = admin_report_repository.get_voucher_usage(
            session=session,
            limit=limit,
        )

        return [
            VoucherUsageItem(
                voucher_id=int(row.get("voucher_id")),
                code=str(row.get("code")),
                discount_type=str(row.get("discount_type")),
                discount_value=float(row.get("discount_value") or 0),
                usage_limit=row.get("usage_limit"),
                used_count=int(row.get("used_count") or 0),
                is_active=bool(row.get("is_active")),
                total_orders_used=int(row.get("total_orders_used") or 0),
            )
            for row in rows
        ]


admin_report_service = AdminReportService()
