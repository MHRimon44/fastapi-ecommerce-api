from typing import List, Optional

from pydantic import BaseModel, Field


class SalesChannelPerformance(BaseModel):
    channel_name: str = Field(..., min_length=2, max_length=100)
    orders: int = Field(..., ge=0)
    sales_amount: float = Field(..., ge=0)


class TopProductPerformance(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=150)
    quantity_sold: int = Field(..., ge=0)
    sales_amount: float = Field(..., ge=0)


class SalesReportAnalysisRequest(BaseModel):
    report_title: str = Field(..., min_length=2, max_length=150)
    start_date: Optional[str] = Field(default=None, max_length=50)
    end_date: Optional[str] = Field(default=None, max_length=50)

    total_orders: int = Field(..., ge=0)
    total_sales_amount: float = Field(..., ge=0)
    total_customers: int = Field(..., ge=0)
    total_products_sold: int = Field(..., ge=0)

    previous_sales_amount: Optional[float] = Field(default=None, ge=0)

    sales_channels: List[SalesChannelPerformance] = Field(default_factory=list)
    top_products: List[TopProductPerformance] = Field(default_factory=list)

    note: Optional[str] = Field(default=None, max_length=500)


class SalesReportAnalysisData(BaseModel):
    summary: str
    average_order_value: float
    sales_growth_percent: Optional[float]
    insights: List[str]
    recommendations: List[str]
    risk_flags: List[str]
    provider: str
    model_name: str


class SalesReportAnalysisResponse(BaseModel):
    message: str
    data: SalesReportAnalysisData
