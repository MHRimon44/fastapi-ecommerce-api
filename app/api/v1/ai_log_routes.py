from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.dependencies.auth_guard import require_authenticated_user
from app.schemas.ai_log_schema import AIRequestLogListResponse
from app.services.ai_log_service import ai_log_service


router = APIRouter(
    prefix="/ai-logs",
    tags=["AI Logs"],
    dependencies=[Depends(require_authenticated_user)],
)


@router.get(
    "/recent",
    response_model=AIRequestLogListResponse,
    status_code=status.HTTP_200_OK,
)
def get_recent_ai_logs(
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
) -> AIRequestLogListResponse:
    data = ai_log_service.get_recent_logs(
        session=session,
        limit=limit,
    )

    return AIRequestLogListResponse(
        message="AI request logs retrieved successfully",
        data=data,
    )
