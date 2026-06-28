from typing import List, Optional

from pydantic import BaseModel, Field


class GenerateProductDescriptionRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=150)
    features: List[str] = Field(..., min_length=1)
    target_audience: Optional[str] = Field(default=None, max_length=100)
    tone: str = Field(default="professional", min_length=2, max_length=50)


class ProductDescriptionData(BaseModel):
    description: str
    bullet_points: List[str]
    provider: str
    model_name: str


class ProductDescriptionResponse(BaseModel):
    message: str
    data: ProductDescriptionData


class SummarizeOrderReportRequest(BaseModel):
    report_title: str = Field(..., min_length=2, max_length=150)
    total_orders: int = Field(..., ge=0)
    total_sales_amount: float = Field(..., ge=0)
    total_customers: int = Field(..., ge=0)
    top_products: List[str] = Field(default_factory=list)
    note: Optional[str] = Field(default=None, max_length=500)


class OrderReportSummaryData(BaseModel):
    summary: str
    insights: List[str]
    provider: str
    model_name: str


class OrderReportSummaryResponse(BaseModel):
    message: str
    data: OrderReportSummaryData


class CustomerSupportReplyRequest(BaseModel):
    customer_name: Optional[str] = Field(default=None, max_length=100)
    order_no: Optional[str] = Field(default=None, max_length=50)
    customer_message: str = Field(..., min_length=5, max_length=1000)
    tone: str = Field(default="polite", min_length=2, max_length=50)


class CustomerSupportReplyData(BaseModel):
    reply: str
    suggested_actions: List[str]
    provider: str
    model_name: str


class CustomerSupportReplyResponse(BaseModel):
    message: str
    data: CustomerSupportReplyData
