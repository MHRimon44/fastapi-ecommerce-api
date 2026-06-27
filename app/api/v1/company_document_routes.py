from fastapi import APIRouter, status

from app.schemas.company_document_schema import (
    CompanyDocumentAskRequest,
    CompanyDocumentAskResponse,
    CompanyDocumentIndexRequest,
    CompanyDocumentIndexResponse,
    CompanyDocumentSearchRequest,
    CompanyDocumentSearchResponse,
)
from app.services.company_document_service import company_document_service


router = APIRouter(
    prefix="/knowledge/company-documents",
    tags=["Company Document Knowledge"],
)


@router.post(
    "/index",
    response_model=CompanyDocumentIndexResponse,
    status_code=status.HTTP_201_CREATED,
)
def index_company_document(
    request: CompanyDocumentIndexRequest,
) -> CompanyDocumentIndexResponse:
    data = company_document_service.index_document(request)

    return CompanyDocumentIndexResponse(
        message="Company document indexed successfully",
        data=data,
    )


@router.post(
    "/search",
    response_model=CompanyDocumentSearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_company_documents(
    request: CompanyDocumentSearchRequest,
) -> CompanyDocumentSearchResponse:
    data = company_document_service.search_documents(request)

    return CompanyDocumentSearchResponse(
        message="Company document search completed successfully",
        data=data,
    )


@router.post(
    "/ask",
    response_model=CompanyDocumentAskResponse,
    status_code=status.HTTP_200_OK,
)
def ask_company_document(
    request: CompanyDocumentAskRequest,
) -> CompanyDocumentAskResponse:
    data = company_document_service.ask_document_question(request)

    return CompanyDocumentAskResponse(
        message="Company document answer generated successfully",
        data=data,
    )
