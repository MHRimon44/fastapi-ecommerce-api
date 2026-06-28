from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.rag_schema import RAGAskData, RAGSearchResult


class ERPPolicyIndexRequest(BaseModel):
    policy_title: str = Field(..., min_length=2, max_length=150)
    module_name: Optional[str] = Field(default=None, max_length=100)
    department: Optional[str] = Field(default=None, max_length=100)
    policy_content: str = Field(..., min_length=20, max_length=5000)
    rules: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class ERPPolicyIndexData(BaseModel):
    document_id: str
    policy_title: str
    chunks_count: int


class ERPPolicyIndexResponse(BaseModel):
    message: str
    data: ERPPolicyIndexData


class ERPPolicySearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class ERPPolicySearchResponse(BaseModel):
    message: str
    data: List[RAGSearchResult]


class ERPPolicyAskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class ERPPolicyAskResponse(BaseModel):
    message: str
    data: RAGAskData
