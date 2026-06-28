from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.rag_schema import RAGAskData, RAGSearchResult


class ProductKnowledgeIndexRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=150)
    sku: Optional[str] = Field(default=None, max_length=100)
    category: Optional[str] = Field(default=None, max_length=100)
    description: str = Field(..., min_length=10, max_length=2000)
    features: List[str] = Field(default_factory=list)
    price: Optional[float] = Field(default=None, ge=0)
    stock_qty: Optional[int] = Field(default=None, ge=0)
    use_case: Optional[str] = Field(default=None, max_length=500)


class ProductKnowledgeIndexData(BaseModel):
    document_id: str
    product_name: str
    chunks_count: int


class ProductKnowledgeIndexResponse(BaseModel):
    message: str
    data: ProductKnowledgeIndexData


class ProductKnowledgeSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class ProductKnowledgeSearchResponse(BaseModel):
    message: str
    data: List[RAGSearchResult]


class ProductKnowledgeAskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class ProductKnowledgeAskResponse(BaseModel):
    message: str
    data: RAGAskData
