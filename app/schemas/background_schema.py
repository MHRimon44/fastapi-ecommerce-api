from pydantic import BaseModel, EmailStr, Field


class EmailTaskRequest(BaseModel):
    to_email: EmailStr
    subject: str = Field(..., min_length=2, max_length=200)
    body: str = Field(..., min_length=2)


class NotificationTaskRequest(BaseModel):
    channel: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=2)


class ReportTaskRequest(BaseModel):
    report_name: str = Field(..., min_length=2, max_length=100)


class AIParseRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=100)
    text: str = Field(..., min_length=2)