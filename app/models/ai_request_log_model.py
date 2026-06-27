from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class AIRequestLog(SQLModel, table=True):
    __tablename__ = "ai_request_logs"

    log_id: Optional[int] = Field(default=None, primary_key=True)

    module_name: str = Field(index=True, max_length=100)
    endpoint: str = Field(index=True, max_length=200)
    status_code: int = Field(index=True)

    user_identifier: Optional[str] = Field(default=None, index=True, max_length=150)

    request_body: str = Field(sa_column=Column(Text, nullable=False))
    response_body: str = Field(sa_column=Column(Text, nullable=False))

    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
