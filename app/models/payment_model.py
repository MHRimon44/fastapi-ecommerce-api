from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.order_model import Order


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    payment_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id", index=True)

    payment_method: str = Field(index=True, max_length=30)
    payment_status: str = Field(index=True, max_length=30)

    amount: float = Field(ge=0)
    transaction_no: Optional[str] = Field(default=None, index=True, max_length=100)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None

    order: Optional["Order"] = Relationship(back_populates="payments")