from fastapi import APIRouter, status

from app.schemas.ai_commerce_schema import (
    AICommerceBusinessReviewRequest,
    AICommerceBusinessReviewResponse,
)
from app.services.ai_commerce_service import ai_commerce_service


router = APIRouter(
    prefix="/ai-commerce",
    tags=["AI Commerce Review"],
)


@router.post(
    "/business-review",
    response_model=AICommerceBusinessReviewResponse,
    status_code=status.HTTP_200_OK,
)
def create_business_review(
    request: AICommerceBusinessReviewRequest,
) -> AICommerceBusinessReviewResponse:
    data = ai_commerce_service.create_business_review(request)

    return AICommerceBusinessReviewResponse(
        message="AI commerce business review generated successfully",
        data=data,
    )
