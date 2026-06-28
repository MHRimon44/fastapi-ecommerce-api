from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    email: str = Field(index=True, max_length=100)
    phone: str = Field(index=True, max_length=20)
    password_hash: str = Field(max_length=255)

    role: str = Field(default="Customer", index=True, max_length=30)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)