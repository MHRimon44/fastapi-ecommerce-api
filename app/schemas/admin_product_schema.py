from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AdminProductCreateRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    sku: Optional[str] = Field(default=None, max_length=100)
    price: float = Field(..., gt=0)
    stock_qty: int = Field(default=0, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = True


class AdminProductUpdateRequest(BaseModel):
    product_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    sku: Optional[str] = Field(default=None, max_length=100)
    price: Optional[float] = Field(default=None, gt=0)
    stock_qty: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)
    is_active: Optional[bool] = None


class AdminProductStockUpdateRequest(BaseModel):
    stock_qty: int = Field(..., ge=0)


class AdminProductStatusUpdateRequest(BaseModel):
    is_active: bool


class AdminProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_name: str
    sku: Optional[str] = None
    price: float
    stock_qty: int
    description: Optional[str] = None
    is_active: bool


class AdminProductSingleResponse(BaseModel):
    message: str
    data: AdminProductResponse


class AdminProductListResponse(BaseModel):
    message: str
    total: int
    page: int
    page_size: int
    data: List[AdminProductResponse]
