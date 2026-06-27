from typing import List, Optional

from pydantic import BaseModel, Field


class RAGDocumentIndexRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    content: str = Field(..., min_length=20)
    source_type: Optional[str] = Field(default="text", max_length=50)


class RAGDocumentIndexData(BaseModel):
    document_id: str
    title: str
    chunks_count: int


class RAGDocumentIndexResponse(BaseModel):
    message: str
    data: RAGDocumentIndexData


class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class RAGSearchResult(BaseModel):
    chunk_id: str
    document_id: str
    title: str
    content: str
    score: float


class RAGSearchResponse(BaseModel):
    message: str
    data: List[RAGSearchResult]


class RAGAskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class RAGAskData(BaseModel):
    answer: str
    sources: List[RAGSearchResult]


class RAGAskResponse(BaseModel):
    message: str
    data: RAGAskData
