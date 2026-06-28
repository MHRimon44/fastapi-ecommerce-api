from typing import List, Optional

from pydantic import BaseModel, Field


class SalesHistoryPoint(BaseModel):
    period: str = Field(..., min_length=2, max_length=50)
    quantity_sold: int = Field(..., ge=0)


class InventoryDemandForecastRequest(BaseModel):
    product_id: Optional[int] = Field(default=None, ge=1)
    product_name: str = Field(..., min_length=2, max_length=150)
    sku: Optional[str] = Field(default=None, max_length=100)
    category: Optional[str] = Field(default=None, max_length=100)

    current_stock_qty: int = Field(..., ge=0)
    reorder_point: int = Field(default=0, ge=0)
    lead_time_days: int = Field(default=7, ge=1)
    safety_stock_qty: int = Field(default=0, ge=0)

    forecast_days: int = Field(default=30, ge=1, le=365)
    sales_history: List[SalesHistoryPoint] = Field(..., min_length=1)

    incoming_stock_qty: int = Field(default=0, ge=0)
    note: Optional[str] = Field(default=None, max_length=500)


class InventoryDemandForecastData(BaseModel):
    product_name: str
    average_daily_sales: float
    forecasted_demand_qty: int
    available_stock_qty: int
    estimated_stock_remaining_days: Optional[float]
    reorder_needed: bool
    suggested_reorder_qty: int
    risk_level: str
    insights: List[str]
    recommendations: List[str]
    provider: str
    model_name: str


class InventoryDemandForecastResponse(BaseModel):
    message: str
    data: InventoryDemandForecastData
