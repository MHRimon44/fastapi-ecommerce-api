from typing import List, Optional

from pydantic import BaseModel, Field


class ProductCandidate(BaseModel):
    product_id: Optional[int] = None
    product_name: str = Field(..., min_length=2, max_length=150)
    sku: Optional[str] = Field(default=None, max_length=100)
    category: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    price: float = Field(..., ge=0)
    stock_qty: int = Field(..., ge=0)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    sales_count: Optional[int] = Field(default=None, ge=0)
    features: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class ProductRecommendationRequest(BaseModel):
    customer_id: Optional[int] = Field(default=None, ge=1)
    customer_segment: Optional[str] = Field(default=None, max_length=100)
    preferred_categories: List[str] = Field(default_factory=list)
    preferred_features: List[str] = Field(default_factory=list)
    previous_purchase_categories: List[str] = Field(default_factory=list)
    budget_min: Optional[float] = Field(default=None, ge=0)
    budget_max: Optional[float] = Field(default=None, ge=0)
    use_case: Optional[str] = Field(default=None, max_length=300)
    top_k: int = Field(default=3, ge=1, le=10)
    products: List[ProductCandidate] = Field(..., min_length=1)


class RecommendedProduct(BaseModel):
    product_id: Optional[int]
    product_name: str
    sku: Optional[str]
    category: Optional[str]
    price: float
    stock_qty: int
    recommendation_score: int
    reasons: List[str]


class ProductRecommendationData(BaseModel):
    recommended_products: List[RecommendedProduct]
    summary: str
    provider: str
    model_name: str


class ProductRecommendationResponse(BaseModel):
    message: str
    data: ProductRecommendationData
