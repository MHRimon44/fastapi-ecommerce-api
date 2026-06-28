from app.providers.ai_provider import get_ai_provider
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
        return get_ai_provider()

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
