import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


BD_PHONE_REGEX = r"^01[3-9]\d{8}$"


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=11, max_length=11)
    password: str = Field(..., min_length=6, max_length=72)

    @field_validator("phone")
    @classmethod
    def validate_bd_phone(cls, value: str) -> str:
        if not re.match(BD_PHONE_REGEX, value):
            raise ValueError(
                "Phone number must be a valid Bangladeshi mobile number. Example: 01700000000"
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password_byte_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password_byte_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")

        return value


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    full_name: str
    email: str
    phone: str
    is_active: bool