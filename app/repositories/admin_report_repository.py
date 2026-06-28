from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlmodel import Session


class AdminReportRepository:
    def get_dashboard_report(
        self,
        session: Session,
    ) -> Dict[str, Any]:
        total_products = self._scalar(
            session,
            "SELECT COUNT(*) FROM products",
        )
        total_customers = self._scalar(
            session,
            "SELECT COUNT(*) FROM customers",
        )
        total_orders = self._scalar(
            session,
            "SELECT COUNT(*) FROM orders",
        )
        total_sales_amount = self._scalar(
            session,
            "SELECT COALESCE(SUM(total_amount), 0) FROM orders",
        )
        total_discount_amount = self._scalar(
            session,
            "SELECT COALESCE(SUM(discount_amount), 0) FROM orders",
        )
        pending_orders = self._scalar(
            session,
            """
            SELECT COUNT(*)
            FROM orders
            WHERE order_status IN ('PLACED', 'PENDING', 'PROCESSING')
            """,
        )
        low_stock_products = self._scalar(
            session,
            """
            SELECT COUNT(*)
            FROM products
            WHERE stock_qty <= 5
            """,
        )
        active_vouchers = self._scalar(
            session,
            """
            SELECT COUNT(*)
            FROM vouchers
            WHERE is_active = :is_active
            """,
            {"is_active": True},
        )

        return {
            "total_products": int(total_products or 0),
            "total_customers": int(total_customers or 0),
            "total_orders": int(total_orders or 0),
            "total_sales_amount": float(total_sales_amount or 0),
            "total_discount_amount": float(total_discount_amount or 0),
            "pending_orders": int(pending_orders or 0),
            "low_stock_products": int(low_stock_products or 0),
            "active_vouchers": int(active_vouchers or 0),
        }

    def get_sales_summary(
        self,
        session: Session,
    ) -> Dict[str, Any]:
        summary = self._one(
            session,
            """
            SELECT
                COUNT(*) AS total_orders,
                COALESCE(SUM(total_amount), 0) AS total_sales_amount,
                COALESCE(SUM(discount_amount), 0) AS total_discount_amount,
                COALESCE(AVG(total_amount), 0) AS average_order_value
            FROM orders
            """,
        )

        by_status = self._all(
            session,
            """
            SELECT
                order_status,
                COUNT(*) AS total_orders,
                COALESCE(SUM(total_amount), 0) AS total_amount
            FROM orders
            GROUP BY order_status
            ORDER BY total_orders DESC
            """,
        )

        by_payment_method = self._all(
            session,
            """
            SELECT
                payment_method,
                COUNT(*) AS total_payments,
                COALESCE(SUM(amount), 0) AS total_amount
            FROM payments
            GROUP BY payment_method
            ORDER BY total_amount DESC
            """,
        )

        return {
            "summary": summary,
            "by_status": by_status,
            "by_payment_method": by_payment_method,
        }

    def get_product_performance(
        self,
        session: Session,
        limit: int,
    ) -> List[Dict[str, Any]]:
        return self._all(
            session,
            """
            SELECT
                p.product_id,
                p.product_name,
                p.sku,
                p.price,
                p.stock_qty AS current_stock_qty,
                COALESCE(SUM(oi.quantity), 0) AS quantity_sold,
                COALESCE(SUM(oi.line_total), 0) AS sales_amount
            FROM products p
            LEFT JOIN order_items oi ON oi.product_id = p.product_id
            GROUP BY
                p.product_id,
                p.product_name,
                p.sku,
                p.price,
                p.stock_qty
            ORDER BY sales_amount DESC, quantity_sold DESC, p.product_id DESC
            LIMIT :limit
            """,
            {"limit": limit},
        )

    def get_voucher_usage(
        self,
        session: Session,
        limit: int,
    ) -> List[Dict[str, Any]]:
        return self._all(
            session,
            """
            SELECT
                v.voucher_id,
                v.code,
                v.discount_type,
                v.discount_value,
                v.usage_limit,
                v.used_count,
                v.is_active,
                COUNT(o.order_id) AS total_orders_used
            FROM vouchers v
            LEFT JOIN orders o ON o.voucher_code = v.code
            GROUP BY
                v.voucher_id,
                v.code,
                v.discount_type,
                v.discount_value,
                v.usage_limit,
                v.used_count,
                v.is_active
            ORDER BY total_orders_used DESC, v.used_count DESC, v.voucher_id DESC
            LIMIT :limit
            """,
            {"limit": limit},
        )

    def _scalar(
        self,
        session: Session,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return session.execute(
            text(query),
            params or {},
        ).scalar()

    def _one(
        self,
        session: Session,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        row = session.execute(
            text(query),
            params or {},
        ).mappings().first()

        return dict(row or {})

    def _all(
        self,
        session: Session,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        rows = session.execute(
            text(query),
            params or {},
        ).mappings().all()

        return [dict(row) for row in rows]


admin_report_repository = AdminReportRepository()
