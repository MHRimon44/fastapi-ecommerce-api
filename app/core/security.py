from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    return password_context.verify(
        plain_password,
        password_hash,
    )


def create_access_token(
    subject: str,
    extra_payload: Optional[Dict[str, Any]] = None,
) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: Dict[str, Any] = {
        "sub": subject,
        "type": "access",
        "exp": expire,
    }

    if extra_payload:
        payload.update(extra_payload)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(
    subject: str,
    extra_payload: Optional[Dict[str, Any]] = None,
) -> str:
    expire = datetime.utcnow() + timedelta(days=7)

    payload: Dict[str, Any] = {
        "sub": subject,
        "type": "refresh",
        "exp": expire,
    }

    if extra_payload:
        payload.update(extra_payload)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None


def decode_access_token(token: str) -> Optional[str]:
    payload = decode_token(token)

    if not payload:
        return None

    if payload.get("type") != "access":
        return None

    return payload.get("sub")


def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    payload = decode_token(token)

    if not payload:
        return None

    if payload.get("type") != "refresh":
        return None

    return payload
