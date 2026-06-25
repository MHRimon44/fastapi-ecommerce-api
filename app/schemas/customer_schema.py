import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


BD_PHONE_REGEX = r"^01[3-9]\d{8}$"


class CustomerCreateRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=11, max_length=11)
    email: Optional[EmailStr] = None

    @field_validator("phone")
    @classmethod
    def validate_bd_phone(cls, value: str) -> str:
        if not re.match(BD_PHONE_REGEX, value):
            raise ValueError(
                "Phone number must be a valid Bangladeshi mobile number. Example: 01700000000"
            )

        return value


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    customer_name: str
    phone: str
    email: Optional[str] = None


class CustomerShortResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    customer_name: str