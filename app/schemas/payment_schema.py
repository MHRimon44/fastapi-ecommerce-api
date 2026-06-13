from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentMethod(str, Enum):
    cod = "COD"
    bkash = "BKASH"
    nagad = "NAGAD"
    card = "CARD"


class PaymentStatus(str, Enum):
    pending = "PENDING"
    paid = "PAID"
    failed = "FAILED"


class PaymentCreateRequest(BaseModel):
    order_id: int = Field(..., gt=0)
    payment_method: PaymentMethod
    transaction_no: Optional[str] = Field(default=None, max_length=100)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    payment_id: int
    order_id: int
    payment_method: str
    payment_status: str
    amount: float
    transaction_no: Optional[str] = None
    created_at: datetime
    paid_at: Optional[datetime] = None


class PaymentListResponse(BaseModel):
    total: int
    items: List[PaymentResponse]