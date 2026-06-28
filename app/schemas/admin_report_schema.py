from typing import List, Optional

from pydantic import BaseModel


class DashboardReportData(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    total_sales_amount: float
    total_discount_amount: float
    pending_orders: int
    low_stock_products: int
    active_vouchers: int


class DashboardReportResponse(BaseModel):
    message: str
    data: DashboardReportData


class OrderStatusSummary(BaseModel):
    order_status: str
    total_orders: int
    total_amount: float


class PaymentMethodSummary(BaseModel):
    payment_method: str
    total_payments: int
    total_amount: float


class SalesSummaryData(BaseModel):
    total_orders: int
    total_sales_amount: float
    total_discount_amount: float
    average_order_value: float
    by_status: List[OrderStatusSummary]
    by_payment_method: List[PaymentMethodSummary]


class SalesSummaryResponse(BaseModel):
    message: str
    data: SalesSummaryData


class ProductPerformanceItem(BaseModel):
    product_id: int
    product_name: str
    sku: Optional[str]
    price: float
    current_stock_qty: int
    quantity_sold: int
    sales_amount: float


class ProductPerformanceResponse(BaseModel):
    message: str
    data: List[ProductPerformanceItem]


class VoucherUsageItem(BaseModel):
    voucher_id: int
    code: str
    discount_type: str
    discount_value: float
    usage_limit: Optional[int]
    used_count: int
    is_active: bool
    total_orders_used: int


class VoucherUsageResponse(BaseModel):
    message: str
    data: List[VoucherUsageItem]
