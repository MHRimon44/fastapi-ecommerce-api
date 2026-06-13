import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60