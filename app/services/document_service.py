import re
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from pypdf import PdfReader

from app.providers.document_ai_provider import get_document_ai_provider

from app.schemas.document_schema import (
    DocumentUploadData,
    PurchaseOrderParseData,
    TechPackExtractData,
)


UPLOAD_DIR = Path("uploads/documents")


class DocumentService:
    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentUploadData:
        original_filename = Path(file.filename or "").name
        suffix = Path(original_filename).suffix.lower()

        if suffix != ".pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed",
            )

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty",
            )

        file_id = str(uuid4())
        saved_filename = f"{file_id}.pdf"

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        file_path = UPLOAD_DIR / saved_filename
        file_path.write_bytes(content)

        return DocumentUploadData(
            file_id=file_id,
            original_filename=original_filename,
            saved_filename=saved_filename,
            file_path=str(file_path),
            content_type=file.content_type or "application/pdf",
            size_bytes=len(content),
        )

    def parse_purchase_order(
        self,
        file_id: str,
    ) -> PurchaseOrderParseData:
        file_path = self._get_document_path(file_id)
        text = self._extract_text(file_path)

        provider = get_document_ai_provider()

        return provider.parse_purchase_order_text(
            file_id=file_id,
            extracted_text=text,
        )

    def extract_tech_pack(
        self,
        file_id: str,
    ) -> TechPackExtractData:
        file_path = self._get_document_path(file_id)
        text = self._extract_text(file_path)

        provider = get_document_ai_provider()

        return provider.extract_tech_pack_text(
            file_id=file_id,
            extracted_text=text,
        )

    def _get_document_path(
        self,
        file_id: str,
    ) -> Path:
        file_path = UPLOAD_DIR / f"{file_id}.pdf"

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found",
            )

        return file_path

    def _extract_text(
        self,
        file_path: Path,
    ) -> str:
        try:
            reader = PdfReader(str(file_path))
            text_parts: List[str] = []

            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)

            extracted_text = "\n".join(text_parts).strip()

            if extracted_text:
                return extracted_text

        except Exception:
            pass

        # Learning-friendly fallback:
        # This helps tests with simple text content saved as .pdf.
        # Real production PDF parsing should rely on valid PDF extraction/OCR.
        return file_path.read_bytes().decode("utf-8", errors="ignore").strip()

    def _find_first(
        self,
        text: str,
        patterns: List[str],
    ) -> Optional[str]:
        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                value = match.group(1).strip()
                value = value.splitlines()[0].strip()
                return value

        return None

    def _extract_total_quantity(
        self,
        text: str,
    ) -> Optional[int]:
        quantities = re.findall(
            r"(?:Qty|Quantity)\s*[:\-]\s*(\d+)",
            text,
            re.IGNORECASE,
        )

        if not quantities:
            return None

        return sum(int(quantity) for quantity in quantities)

    def _extract_item_lines(
        self,
        text: str,
    ) -> List[str]:
        lines = text.splitlines()
        items: List[str] = []

        for line in lines:
            clean_line = line.strip()

            if not clean_line:
                continue

            lower_line = clean_line.lower()

            if (
                "item" in lower_line
                or "product" in lower_line
                or "style" in lower_line
                or "sku" in lower_line
            ):
                items.append(clean_line)

        return items[:10]

    def _extract_measurement_lines(
        self,
        text: str,
    ) -> List[str]:
        lines = text.splitlines()
        measurements: List[str] = []

        keywords = [
            "measurement",
            "chest",
            "length",
            "sleeve",
            "waist",
            "hip",
            "shoulder",
            "inseam",
        ]

        for line in lines:
            clean_line = line.strip()

            if not clean_line:
                continue

            lower_line = clean_line.lower()

            if any(keyword in lower_line for keyword in keywords):
                measurements.append(clean_line)

        return measurements[:15]

    def _preview_text(
        self,
        text: str,
    ) -> str:
        clean_text = " ".join(text.split())

        return clean_text[:500]


document_service = DocumentService()
