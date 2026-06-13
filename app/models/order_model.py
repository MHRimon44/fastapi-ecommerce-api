from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.customer_model import Customer
    from app.models.payment_model import Payment

class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: Optional[int] = Field(default=None, primary_key=True)
    order_no: str = Field(index=True, max_length=50)
    customer_id: int = Field(foreign_key="customers.customer_id", index=True)
    order_status: str = Field(default="PLACED", index=True, max_length=30)
    sub_total: float = Field(default=0, ge=0)
    discount_amount: float = Field(default=0, ge=0)
    total_amount: float = Field(default=0, ge=0)
    voucher_code: Optional[str] = Field(default=None, index=True, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    customer: Optional["Customer"] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")
    payments: List["Payment"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    order_item_id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.order_id", index=True)
    product_id: int = Field(foreign_key="products.product_id", index=True)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    line_total: float = Field(ge=0)

    order: Optional["Order"] = Relationship(back_populates="items")