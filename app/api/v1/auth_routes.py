from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.db.session import get_session
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.schemas.common_schema import MessageResponse
from app.services.auth_service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    session: Session = Depends(get_session),
):
    auth_service.register(
        session=session,
        request=request,
    )

    return MessageResponse(
        message="User registered successfully",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
):
    return auth_service.login(
        session=session,
        request=request,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)