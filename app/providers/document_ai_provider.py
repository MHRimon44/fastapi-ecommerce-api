import json
import re
from typing import List, Optional

from fastapi import HTTPException, status

from app.core.config import settings
from app.prompts.document_prompts import (
    build_purchase_order_parse_prompt,
    build_tech_pack_extract_prompt,
)
from app.schemas.document_schema import (
    PurchaseOrderParseData,
    TechPackExtractData,
)


class MockDocumentAIProvider:
    def parse_purchase_order_text(
        self,
        file_id: str,
        extracted_text: str,
    ) -> PurchaseOrderParseData:
        return PurchaseOrderParseData(
            document_type="purchase_order",
            file_id=file_id,
            po_number=self._find_first(
                extracted_text,
                [
                    r"PO\s*(?:Number|No|#)\s*[:\-]\s*([^\n\r]+)",
                    r"Purchase\s*Order\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            buyer_name=self._find_first(
                extracted_text,
                [
                    r"Buyer\s*[:\-]\s*([^\n\r]+)",
                    r"Customer\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            supplier_name=self._find_first(
                extracted_text,
                [
                    r"Supplier\s*[:\-]\s*([^\n\r]+)",
                    r"Vendor\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            order_date=self._find_first(
                extracted_text,
                [
                    r"Order\s*Date\s*[:\-]\s*([^\n\r]+)",
                    r"Date\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            total_quantity=self._extract_total_quantity(extracted_text),
            items=self._extract_item_lines(extracted_text),
            extracted_text_preview=self._preview_text(extracted_text),
        )

    def extract_tech_pack_text(
        self,
        file_id: str,
        extracted_text: str,
    ) -> TechPackExtractData:
        return TechPackExtractData(
            document_type="tech_pack",
            file_id=file_id,
            style_no=self._find_first(
                extracted_text,
                [
                    r"Style\s*(?:No|Number|#)\s*[:\-]\s*([^\n\r]+)",
                    r"Style\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            buyer_name=self._find_first(
                extracted_text,
                [
                    r"Buyer\s*[:\-]\s*([^\n\r]+)",
                    r"Customer\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            product_type=self._find_first(
                extracted_text,
                [
                    r"Product\s*Type\s*[:\-]\s*([^\n\r]+)",
                    r"Garment\s*Type\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            fabric=self._find_first(
                extracted_text,
                [
                    r"Fabric\s*[:\-]\s*([^\n\r]+)",
                    r"Material\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            color=self._find_first(
                extracted_text,
                [
                    r"Color\s*[:\-]\s*([^\n\r]+)",
                    r"Colour\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            size_range=self._find_first(
                extracted_text,
                [
                    r"Size\s*Range\s*[:\-]\s*([^\n\r]+)",
                    r"Sizes\s*[:\-]\s*([^\n\r]+)",
                ],
            ),
            measurements=self._extract_measurement_lines(extracted_text),
            extracted_text_preview=self._preview_text(extracted_text),
        )

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
                return match.group(1).strip().splitlines()[0].strip()

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
        items: List[str] = []

        for line in text.splitlines():
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

        for line in text.splitlines():
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
        return " ".join(text.split())[:500]


class OpenAIDocumentAIProvider:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured",
            )

        from openai import OpenAI

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=30.0,
        )

    def parse_purchase_order_text(
        self,
        file_id: str,
        extracted_text: str,
    ) -> PurchaseOrderParseData:
        prompt = build_purchase_order_parse_prompt(extracted_text)
        data = self._request_json_from_ai(prompt)

        return PurchaseOrderParseData(
            document_type="purchase_order",
            file_id=file_id,
            po_number=data.get("po_number"),
            buyer_name=data.get("buyer_name"),
            supplier_name=data.get("supplier_name"),
            order_date=data.get("order_date"),
            total_quantity=data.get("total_quantity"),
            items=data.get("items", []),
            extracted_text_preview=self._preview_text(extracted_text),
        )

    def extract_tech_pack_text(
        self,
        file_id: str,
        extracted_text: str,
    ) -> TechPackExtractData:
        prompt = build_tech_pack_extract_prompt(extracted_text)
        data = self._request_json_from_ai(prompt)

        return TechPackExtractData(
            document_type="tech_pack",
            file_id=file_id,
            style_no=data.get("style_no"),
            buyer_name=data.get("buyer_name"),
            product_type=data.get("product_type"),
            fabric=data.get("fabric"),
            color=data.get("color"),
            size_range=data.get("size_range"),
            measurements=data.get("measurements", []),
            extracted_text_preview=self._preview_text(extracted_text),
        )

    def _request_json_from_ai(
        self,
        prompt: str,
    ) -> dict:
        try:
            response = self.client.responses.create(
                model=settings.AI_MODEL_NAME,
                instructions=(
                    "You are a document parsing assistant. "
                    "Return only valid JSON. Do not include markdown."
                ),
                input=prompt,
            )

            return json.loads(response.output_text)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned invalid JSON",
            )

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider request failed",
            )

    def _preview_text(
        self,
        text: str,
    ) -> str:
        return " ".join(text.split())[:500]


def get_document_ai_provider():
    if settings.AI_PROVIDER == "mock":
        return MockDocumentAIProvider()

    if settings.AI_PROVIDER == "openai":
        return OpenAIDocumentAIProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported AI provider",
    )
