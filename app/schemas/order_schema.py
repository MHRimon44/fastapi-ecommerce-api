from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreateRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreateRequest(BaseModel):
    customer_id: int = Field(..., gt=0)
    items: List[OrderItemCreateRequest] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_item_id: int
    product_id: int
    quantity: int
    unit_price: float
    line_total: float


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    order_no: str
    customer_id: int
    order_status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]

class OrderCreateResponse(BaseModel):
    message: str
    order_no: str
    data: OrderResponse