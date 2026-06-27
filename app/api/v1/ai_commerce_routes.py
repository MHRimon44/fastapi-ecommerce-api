from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.dependencies.auth_guard import require_authenticated_user
from app.schemas.ai_commerce_schema import (
    AICommerceBusinessReviewRequest,
    AICommerceBusinessReviewResponse,
)
from app.services.ai_commerce_service import ai_commerce_service
from app.services.ai_log_service import ai_log_service


router = APIRouter(
    prefix="/ai-commerce",
    tags=["AI Commerce Review"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.post(
    "/business-review",
    response_model=AICommerceBusinessReviewResponse,
    status_code=status.HTTP_200_OK,
)
def create_business_review(
    request: AICommerceBusinessReviewRequest,
    session: Session = Depends(get_session),
) -> AICommerceBusinessReviewResponse:
    data = ai_commerce_service.create_business_review(request)

    response = AICommerceBusinessReviewResponse(
        message="AI commerce business review generated successfully",
        data=data,
    )

    ai_log_service.save_log(
        session=session,
        module_name="AI_COMMERCE_BUSINESS_REVIEW",
        endpoint="/ai-commerce/business-review",
        request_payload=request.model_dump(mode="json"),
        response_payload=response.model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )

    return response
