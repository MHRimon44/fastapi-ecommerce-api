from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.rag_schema import RAGAskData, RAGSearchResult


class SupportKnowledgeIndexRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    issue_type: Optional[str] = Field(default=None, max_length=100)
    content: str = Field(..., min_length=20, max_length=3000)
    resolution_steps: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class SupportKnowledgeIndexData(BaseModel):
    document_id: str
    title: str
    chunks_count: int


class SupportKnowledgeIndexResponse(BaseModel):
    message: str
    data: SupportKnowledgeIndexData


class SupportKnowledgeSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class SupportKnowledgeSearchResponse(BaseModel):
    message: str
    data: List[RAGSearchResult]


class SupportKnowledgeAskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class SupportKnowledgeAskResponse(BaseModel):
    message: str
    data: RAGAskData
