from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Voucher(SQLModel, table=True):
    __tablename__ = "vouchers"

    voucher_id: Optional[int] = Field(default=None, primary_key=True)

    code: str = Field(index=True, max_length=50)
    discount_type: str = Field(index=True, max_length=20)

    discount_value: float = Field(gt=0)
    min_order_amount: float = Field(default=0, ge=0)
    max_discount_amount: Optional[float] = Field(default=None, ge=0)

    usage_limit: Optional[int] = Field(default=None, ge=1)
    used_count: int = Field(default=0, ge=0)

    is_active: bool = Field(default=True, index=True)

    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)