from fastapi import APIRouter, File, UploadFile, status, Depends

from app.schemas.document_schema import (
    DocumentParseRequest,
    DocumentUploadResponse,
    PurchaseOrderParseResponse,
    TechPackExtractResponse,
)
from app.services.document_service import document_service
from app.dependencies.auth_guard import require_authenticated_user


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.post(
    "/upload",
    response_model=DocumentUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
) -> DocumentUploadResponse:
    data = await document_service.upload_document(file)

    return DocumentUploadResponse(
        message="Document uploaded successfully",
        data=data,
    )


@router.post(
    "/parse-purchase-order",
    response_model=PurchaseOrderParseResponse,
    status_code=status.HTTP_200_OK,
)
def parse_purchase_order(
    request: DocumentParseRequest,
) -> PurchaseOrderParseResponse:
    data = document_service.parse_purchase_order(request.file_id)

    return PurchaseOrderParseResponse(
        message="Purchase order parsed successfully",
        data=data,
    )


@router.post(
    "/extract-tech-pack",
    response_model=TechPackExtractResponse,
    status_code=status.HTTP_200_OK,
)
def extract_tech_pack(
    request: DocumentParseRequest,
) -> TechPackExtractResponse:
    data = document_service.extract_tech_pack(request.file_id)

    return TechPackExtractResponse(
        message="Tech pack extracted successfully",
        data=data,
    )
