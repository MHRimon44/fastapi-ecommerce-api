from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class OrderPlacedResponse(BaseModel):
    message: str
    order_no: str