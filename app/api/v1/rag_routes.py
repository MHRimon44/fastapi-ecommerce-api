from fastapi import APIRouter, status

from app.schemas.rag_schema import (
    RAGAskRequest,
    RAGAskResponse,
    RAGDocumentIndexRequest,
    RAGDocumentIndexResponse,
    RAGSearchRequest,
    RAGSearchResponse,
)
from app.services.rag_service import rag_service


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/documents/index",
    response_model=RAGDocumentIndexResponse,
    status_code=status.HTTP_201_CREATED,
)
def index_document(
    request: RAGDocumentIndexRequest,
) -> RAGDocumentIndexResponse:
    data = rag_service.index_document(request)

    return RAGDocumentIndexResponse(
        message="Document indexed successfully",
        data=data,
    )


@router.post(
    "/search",
    response_model=RAGSearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_documents(
    request: RAGSearchRequest,
) -> RAGSearchResponse:
    data = rag_service.search(
        query=request.query,
        top_k=request.top_k,
    )

    return RAGSearchResponse(
        message="Search completed successfully",
        data=data,
    )


@router.post(
    "/ask",
    response_model=RAGAskResponse,
    status_code=status.HTTP_200_OK,
)
def ask_question(
    request: RAGAskRequest,
) -> RAGAskResponse:
    data = rag_service.ask(
        question=request.question,
        top_k=request.top_k,
    )

    return RAGAskResponse(
        message="Answer generated successfully",
        data=data,
    )
