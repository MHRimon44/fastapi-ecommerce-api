from typing import List, Optional

from pydantic import BaseModel, Field


class CustomerVoucherUsagePattern(BaseModel):
    customer_id: int = Field(..., ge=1)
    customer_name: Optional[str] = Field(default=None, max_length=100)
    usage_count: int = Field(..., ge=0)
    total_discount_amount: float = Field(..., ge=0)
    total_order_amount: float = Field(..., ge=0)


class VoucherFraudDetectRequest(BaseModel):
    voucher_code: str = Field(..., min_length=2, max_length=50)
    discount_type: str = Field(..., min_length=2, max_length=20)
    discount_value: float = Field(..., ge=0)

    min_order_amount: float = Field(default=0, ge=0)
    max_discount_amount: Optional[float] = Field(default=None, ge=0)

    usage_limit: Optional[int] = Field(default=None, ge=0)
    used_count: int = Field(..., ge=0)

    total_orders_using_voucher: int = Field(..., ge=0)
    total_discount_given: float = Field(..., ge=0)
    total_sales_amount: float = Field(..., ge=0)

    unique_customers_used: int = Field(..., ge=0)
    repeated_customers_count: int = Field(..., ge=0)
    suspicious_order_count: int = Field(default=0, ge=0)

    customer_patterns: List[CustomerVoucherUsagePattern] = Field(default_factory=list)
    note: Optional[str] = Field(default=None, max_length=500)


class VoucherFraudDetectData(BaseModel):
    risk_score: int
    risk_level: str
    is_suspicious: bool
    signals: List[str]
    recommendations: List[str]
    provider: str
    model_name: str


class VoucherFraudDetectResponse(BaseModel):
    message: str
    data: VoucherFraudDetectData
