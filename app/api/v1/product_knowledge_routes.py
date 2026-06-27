from fastapi import APIRouter, status

from app.schemas.product_knowledge_schema import (
    ProductKnowledgeAskRequest,
    ProductKnowledgeAskResponse,
    ProductKnowledgeIndexRequest,
    ProductKnowledgeIndexResponse,
    ProductKnowledgeSearchRequest,
    ProductKnowledgeSearchResponse,
)
from app.services.product_knowledge_service import product_knowledge_service


router = APIRouter(
    prefix="/knowledge/products",
    tags=["Product Knowledge"],
)


@router.post(
    "/index",
    response_model=ProductKnowledgeIndexResponse,
    status_code=status.HTTP_201_CREATED,
)
def index_product_knowledge(
    request: ProductKnowledgeIndexRequest,
) -> ProductKnowledgeIndexResponse:
    data = product_knowledge_service.index_product(request)

    return ProductKnowledgeIndexResponse(
        message="Product knowledge indexed successfully",
        data=data,
    )


@router.post(
    "/search",
    response_model=ProductKnowledgeSearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_product_knowledge(
    request: ProductKnowledgeSearchRequest,
) -> ProductKnowledgeSearchResponse:
    data = product_knowledge_service.search_products(request)

    return ProductKnowledgeSearchResponse(
        message="Product knowledge search completed successfully",
        data=data,
    )


@router.post(
    "/ask",
    response_model=ProductKnowledgeAskResponse,
    status_code=status.HTTP_200_OK,
)
def ask_product_knowledge(
    request: ProductKnowledgeAskRequest,
) -> ProductKnowledgeAskResponse:
    data = product_knowledge_service.ask_product_question(request)

    return ProductKnowledgeAskResponse(
        message="Product knowledge answer generated successfully",
        data=data,
    )
