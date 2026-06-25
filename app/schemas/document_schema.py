from typing import List, Optional

from pydantic import BaseModel, Field


class DocumentUploadData(BaseModel):
    file_id: str
    original_filename: str
    saved_filename: str
    file_path: str
    content_type: str
    size_bytes: int


class DocumentUploadResponse(BaseModel):
    message: str
    data: DocumentUploadData


class DocumentParseRequest(BaseModel):
    file_id: str = Field(..., min_length=10)


class PurchaseOrderParseData(BaseModel):
    document_type: str
    file_id: str
    po_number: Optional[str] = None
    buyer_name: Optional[str] = None
    supplier_name: Optional[str] = None
    order_date: Optional[str] = None
    total_quantity: Optional[int] = None
    items: List[str]
    extracted_text_preview: str


class PurchaseOrderParseResponse(BaseModel):
    message: str
    data: PurchaseOrderParseData


class TechPackExtractData(BaseModel):
    document_type: str
    file_id: str
    style_no: Optional[str] = None
    buyer_name: Optional[str] = None
    product_type: Optional[str] = None
    fabric: Optional[str] = None
    color: Optional[str] = None
    size_range: Optional[str] = None
    measurements: List[str]
    extracted_text_preview: str


class TechPackExtractResponse(BaseModel):
    message: str
    data: TechPackExtractData
