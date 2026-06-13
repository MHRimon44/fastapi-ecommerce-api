from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DiscountType(str, Enum):
    flat = "FLAT"
    percentage = "PERCENTAGE"


class VoucherCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=50)
    discount_type: DiscountType
    discount_value: float = Field(..., gt=0)

    min_order_amount: float = Field(default=0, ge=0)
    max_discount_amount: Optional[float] = Field(default=None, ge=0)

    usage_limit: Optional[int] = Field(default=None, ge=1)

    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None


class VoucherApplyRequest(BaseModel):
    order_id: int = Field(..., gt=0)
    voucher_code: str = Field(..., min_length=2, max_length=50)


class VoucherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    voucher_id: int
    code: str
    discount_type: str
    discount_value: float
    min_order_amount: float
    max_discount_amount: Optional[float] = None
    usage_limit: Optional[int] = None
    used_count: int
    is_active: bool
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None


class VoucherListResponse(BaseModel):
    total: int
    items: List[VoucherResponse]