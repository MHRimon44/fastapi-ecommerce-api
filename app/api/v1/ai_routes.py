from fastapi import APIRouter, status, Depends

from app.schemas.ai_schema import (
    CustomerSupportReplyRequest,
    CustomerSupportReplyResponse,
    GenerateProductDescriptionRequest,
    OrderReportSummaryResponse,
    ProductDescriptionResponse,
    SummarizeOrderReportRequest,
)
from app.services.ai_service import ai_service
from app.dependencies.auth_guard import require_authenticated_user


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.post(
    "/generate-product-description",
    response_model=ProductDescriptionResponse,
    status_code=status.HTTP_200_OK,
)
def generate_product_description(
    request: GenerateProductDescriptionRequest,
) -> ProductDescriptionResponse:
    data = ai_service.generate_product_description(request)

    return ProductDescriptionResponse(
        message="Product description generated successfully",
        data=data,
    )


@router.post(
    "/summarize-order-report",
    response_model=OrderReportSummaryResponse,
    status_code=status.HTTP_200_OK,
)
def summarize_order_report(
    request: SummarizeOrderReportRequest,
) -> OrderReportSummaryResponse:
    data = ai_service.summarize_order_report(request)

    return OrderReportSummaryResponse(
        message="Order report summarized successfully",
        data=data,
    )


@router.post(
    "/customer-support-reply",
    response_model=CustomerSupportReplyResponse,
    status_code=status.HTTP_200_OK,
)
def generate_customer_support_reply(
    request: CustomerSupportReplyRequest,
) -> CustomerSupportReplyResponse:
    data = ai_service.generate_customer_support_reply(request)

    return CustomerSupportReplyResponse(
        message="Customer support reply generated successfully",
        data=data,
    )
