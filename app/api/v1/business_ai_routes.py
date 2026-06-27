from fastapi import APIRouter, status

from app.schemas.business_ai_schema import (
    SalesReportAnalysisRequest,
    SalesReportAnalysisResponse,
)
from app.services.business_ai_service import business_ai_service


router = APIRouter(
    prefix="/business-ai",
    tags=["Business AI"],
)


@router.post(
    "/sales-report/analyze",
    response_model=SalesReportAnalysisResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_sales_report(
    request: SalesReportAnalysisRequest,
) -> SalesReportAnalysisResponse:
    data = business_ai_service.analyze_sales_report(request)

    return SalesReportAnalysisResponse(
        message="Sales report analyzed successfully",
        data=data,
    )
