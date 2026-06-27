from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.rag_schema import RAGAskData, RAGSearchResult


class CompanyDocumentIndexRequest(BaseModel):
    document_title: str = Field(..., min_length=2, max_length=150)
    department: Optional[str] = Field(default=None, max_length=100)
    document_type: Optional[str] = Field(default=None, max_length=100)
    content: str = Field(..., min_length=20, max_length=8000)
    tags: List[str] = Field(default_factory=list)


class CompanyDocumentIndexData(BaseModel):
    document_id: str
    document_title: str
    chunks_count: int


class CompanyDocumentIndexResponse(BaseModel):
    message: str
    data: CompanyDocumentIndexData


class CompanyDocumentSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class CompanyDocumentSearchResponse(BaseModel):
    message: str
    data: List[RAGSearchResult]


class CompanyDocumentAskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class CompanyDocumentAskResponse(BaseModel):
    message: str
    data: RAGAskData
