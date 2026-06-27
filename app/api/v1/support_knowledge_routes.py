from fastapi import APIRouter, status

from app.schemas.support_knowledge_schema import (
    SupportKnowledgeAskRequest,
    SupportKnowledgeAskResponse,
    SupportKnowledgeIndexRequest,
    SupportKnowledgeIndexResponse,
    SupportKnowledgeSearchRequest,
    SupportKnowledgeSearchResponse,
)
from app.services.support_knowledge_service import support_knowledge_service


router = APIRouter(
    prefix="/knowledge/support",
    tags=["Customer Support Knowledge"],
)


@router.post(
    "/index",
    response_model=SupportKnowledgeIndexResponse,
    status_code=status.HTTP_201_CREATED,
)
def index_support_knowledge(
    request: SupportKnowledgeIndexRequest,
) -> SupportKnowledgeIndexResponse:
    data = support_knowledge_service.index_support_knowledge(request)

    return SupportKnowledgeIndexResponse(
        message="Support knowledge indexed successfully",
        data=data,
    )


@router.post(
    "/search",
    response_model=SupportKnowledgeSearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_support_knowledge(
    request: SupportKnowledgeSearchRequest,
) -> SupportKnowledgeSearchResponse:
    data = support_knowledge_service.search_support_knowledge(request)

    return SupportKnowledgeSearchResponse(
        message="Support knowledge search completed successfully",
        data=data,
    )


@router.post(
    "/ask",
    response_model=SupportKnowledgeAskResponse,
    status_code=status.HTTP_200_OK,
)
def ask_support_knowledge(
    request: SupportKnowledgeAskRequest,
) -> SupportKnowledgeAskResponse:
    data = support_knowledge_service.ask_support_question(request)

    return SupportKnowledgeAskResponse(
        message="Support knowledge answer generated successfully",
        data=data,
    )
