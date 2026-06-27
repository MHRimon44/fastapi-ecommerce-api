from app.providers.business_ai_provider import get_business_ai_provider
from app.schemas.business_ai_schema import (
    SalesReportAnalysisData,
    SalesReportAnalysisRequest,
)


class BusinessAIService:
    def analyze_sales_report(
        self,
        request: SalesReportAnalysisRequest,
    ) -> SalesReportAnalysisData:
        provider = get_business_ai_provider()

        return provider.analyze_sales_report(request)


business_ai_service = BusinessAIService()
