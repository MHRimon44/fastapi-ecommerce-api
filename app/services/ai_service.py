from fastapi import HTTPException, status

from app.core.config import settings
from app.providers.ai_provider import MockAIProvider, OpenAIProvider
from app.schemas.ai_schema import (
    CustomerSupportReplyData,
    CustomerSupportReplyRequest,
    GenerateProductDescriptionRequest,
    OrderReportSummaryData,
    ProductDescriptionData,
    SummarizeOrderReportRequest,
)


class AIService:
    def _get_provider(self):
        if settings.AI_PROVIDER == "mock":
            return MockAIProvider()

        if settings.AI_PROVIDER == "openai":
            return OpenAIProvider()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported AI provider",
        )

    def generate_product_description(
        self,
        request: GenerateProductDescriptionRequest,
    ) -> ProductDescriptionData:
        provider = self._get_provider()
        return provider.generate_product_description(request)

    def summarize_order_report(
        self,
        request: SummarizeOrderReportRequest,
    ) -> OrderReportSummaryData:
        provider = self._get_provider()
        return provider.summarize_order_report(request)

    def generate_customer_support_reply(
        self,
        request: CustomerSupportReplyRequest,
    ) -> CustomerSupportReplyData:
        provider = self._get_provider()
        return provider.generate_customer_support_reply(request)


ai_service = AIService()
