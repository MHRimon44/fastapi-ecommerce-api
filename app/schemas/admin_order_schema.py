from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AdminOrderStatusUpdateRequest(BaseModel):
    order_status: str = Field(..., min_length=2, max_length=30)


class AdminOrderCustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    customer_name: str
    phone: str
    email: Optional[str] = None


class AdminOrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_item_id: int
    order_id: int
    product_id: int
    product_name: Optional[str] = None
    quantity: int
    unit_price: float
    line_total: float


class AdminOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    order_no: str
    customer_id: int
    order_status: str
    sub_total: float
    discount_amount: float
    total_amount: float
    voucher_code: Optional[str] = None
    created_at: datetime


class AdminOrderDetailResponseData(BaseModel):
    order: AdminOrderResponse
    customer: Optional[AdminOrderCustomerResponse] = None
    items: List[AdminOrderItemResponse]


class AdminOrderListResponse(BaseModel):
    message: str
    total: int
    page: int
    page_size: int
    data: List[AdminOrderResponse]


class AdminOrderSingleResponse(BaseModel):
    message: str
    data: AdminOrderDetailResponseData


class AdminOrderItemsResponse(BaseModel):
    message: str
    total: int
    data: List[AdminOrderItemResponse]
