from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.order_model import Order


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    customer_id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str = Field(index=True, max_length=100)
    phone: str = Field(index=True, max_length=20)
    email: Optional[str] = Field(default=None, index=True, max_length=100)

    orders: List["Order"] = Relationship(back_populates="customer")