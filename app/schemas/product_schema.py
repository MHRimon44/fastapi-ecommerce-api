from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class ProductSortOption(str, Enum):
    default = "default"
    high_to_low = "high_to_low"
    low_to_high = "low_to_high"
    newly_added = "newly_added"


class ProductCreateRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_qty: int = Field(..., ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class ProductUpdateRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_qty: int = Field(..., ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class ProductPatchRequest(BaseModel):
    product_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    price: Optional[float] = Field(default=None, gt=0)
    stock_qty: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = Field(default=None, max_length=500)


class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    price: float
    stock_qty: int
    description: Optional[str] = None


class ProductListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[ProductResponse]