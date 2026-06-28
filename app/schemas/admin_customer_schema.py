import re
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


BD_PHONE_PATTERN = re.compile(r"^(?:\+8801|8801|01)[3-9][0-9]{8}$")


def normalize_bd_phone(phone: str) -> str:
    phone_value = phone.strip().replace(" ", "").replace("-", "")

    if phone_value.startswith("+880"):
        phone_value = "0" + phone_value[4:]

    if phone_value.startswith("880"):
        phone_value = "0" + phone_value[3:]

    return phone_value


class AdminCustomerCreateRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=11, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        normalized_phone = normalize_bd_phone(value)

        if not BD_PHONE_PATTERN.match(normalized_phone):
            raise ValueError("Invalid Bangladesh phone number")

        return normalized_phone


class AdminCustomerUpdateRequest(BaseModel):
    customer_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, min_length=11, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        normalized_phone = normalize_bd_phone(value)

        if not BD_PHONE_PATTERN.match(normalized_phone):
            raise ValueError("Invalid Bangladesh phone number")

        return normalized_phone


class AdminCustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    customer_name: str
    phone: str
    email: Optional[str] = None


class AdminCustomerSingleResponse(BaseModel):
    message: str
    data: AdminCustomerResponse


class AdminCustomerListResponse(BaseModel):
    message: str
    total: int
    page: int
    page_size: int
    data: List[AdminCustomerResponse]
