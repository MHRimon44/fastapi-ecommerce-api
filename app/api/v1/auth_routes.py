from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.db.session import get_session
from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from app.schemas.auth_schema import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenPairResponse,
    TokenResponse,
    UserResponse,
)
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


@router.post(
    "/refresh",
    response_model=TokenPairResponse,
)
def refresh_token(
    request: RefreshTokenRequest,
) -> TokenPairResponse:
    payload = decode_refresh_token(request.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    subject = payload.get("sub")

    token_payload = {
        "user_id": payload.get("user_id"),
        "email": payload.get("email"),
        "role": payload.get("role"),
    }

    access_token = create_access_token(
        subject=subject,
        extra_payload=token_payload,
    )

    refresh_token_value = create_refresh_token(
        subject=subject,
        extra_payload=token_payload,
    )

    return TokenPairResponse(
        message="Token refreshed successfully",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_value,
            token_type="bearer",
        ),
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)
