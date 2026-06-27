from typing import List, Optional

from pydantic import BaseModel, Field


class CustomerSegmentationRequest(BaseModel):
    customer_id: Optional[int] = Field(default=None, ge=1)
    customer_name: Optional[str] = Field(default=None, max_length=100)

    total_orders: int = Field(..., ge=0)
    total_spent: float = Field(..., ge=0)
    average_order_value: float = Field(..., ge=0)

    days_since_last_order: Optional[int] = Field(default=None, ge=0)
    return_order_count: int = Field(default=0, ge=0)
    cancelled_order_count: int = Field(default=0, ge=0)

    used_voucher_count: int = Field(default=0, ge=0)
    total_discount_received: float = Field(default=0, ge=0)

    preferred_categories: List[str] = Field(default_factory=list)
    preferred_channels: List[str] = Field(default_factory=list)

    note: Optional[str] = Field(default=None, max_length=500)


class CustomerSegmentationData(BaseModel):
    segment_name: str
    segment_score: int
    customer_value_level: str
    insights: List[str]
    recommendations: List[str]
    risk_flags: List[str]
    provider: str
    model_name: str


class CustomerSegmentationResponse(BaseModel):
    message: str
    data: CustomerSegmentationData
