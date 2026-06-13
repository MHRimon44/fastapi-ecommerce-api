from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import user_repository
from app.schemas.auth_schema import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def register(
        self,
        session: Session,
        request: RegisterRequest,
    ) -> None:
        existing_user = user_repository.get_by_email(
            session=session,
            email=request.email,
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        password_hash = hash_password(request.password)

        user_repository.create_user(
            session=session,
            full_name=request.full_name,
            email=request.email,
            phone=request.phone,
            password_hash=password_hash,
        )

    def login(
        self,
        session: Session,
        request: LoginRequest,
    ) -> TokenResponse:
        user = user_repository.get_by_email(
            session=session,
            email=request.email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        is_password_valid = verify_password(
            plain_password=request.password,
            password_hash=user.password_hash,
        )

        if not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(subject=str(user.user_id))

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )


auth_service = AuthService()