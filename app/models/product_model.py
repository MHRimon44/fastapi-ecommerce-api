from typing import Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "products"

    product_id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str = Field(index=True, max_length=100)
    sku: Optional[str] = Field(default=None, index=True, max_length=100)
    price: float = Field(index=True, gt=0)
    stock_qty: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True, index=True)
    description: Optional[str] = Field(default=None, max_length=500)
