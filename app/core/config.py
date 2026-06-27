import os
from typing import List, Optional

from dotenv import load_dotenv


load_dotenv()


def _get_bool(key: str, default: bool = False) -> bool:
    value = os.getenv(key)

    if value is None:
        return default

    return value.lower() in ["true", "1", "yes", "y"]


def _get_int(key: str, default: int) -> int:
    value = os.getenv(key)

    if value is None:
        return default

    return int(value)


def _get_list(key: str, default: str = "") -> List[str]:
    value = os.getenv(key, default)

    if not value:
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "FastAPI Ecommerce")
        self.APP_ENV = os.getenv("APP_ENV", "local")
        self.DEBUG = _get_bool("DEBUG", True)

        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "sqlite:///./ecommerce.db",
        )

        self.SECRET_KEY = os.getenv(
            "SECRET_KEY",
            "CHANGE_THIS_SECRET_KEY_FOR_PRODUCTION",
        )
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = _get_int(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            60,
        )

        self.CORS_ALLOWED_ORIGINS = _get_list(
            "CORS_ALLOWED_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )

        self.AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
        self.AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "mock-product-writer-v1")
        self.OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

        self.EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "mock")
        self.EMBEDDING_MODEL_NAME = os.getenv(
            "EMBEDDING_MODEL_NAME",
            "mock-bow-v1",
        )


settings = Settings()


# Backward compatibility for old imports
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
DATABASE_URL = settings.DATABASE_URL
