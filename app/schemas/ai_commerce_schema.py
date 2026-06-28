from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from app.schemas.business_ai_schema import SalesReportAnalysisRequest
from app.schemas.customer_segmentation_schema import CustomerSegmentationRequest
from app.schemas.inventory_demand_schema import InventoryDemandForecastRequest
from app.schemas.product_recommendation_schema import ProductRecommendationRequest
from app.schemas.voucher_fraud_schema import VoucherFraudDetectRequest


class AICommerceBusinessReviewRequest(BaseModel):
    review_title: str = Field(..., min_length=2, max_length=150)

    sales_report: Optional[SalesReportAnalysisRequest] = None
    voucher_fraud: Optional[VoucherFraudDetectRequest] = None
    product_recommendation: Optional[ProductRecommendationRequest] = None

    inventory_forecasts: List[InventoryDemandForecastRequest] = Field(
        default_factory=list
    )
    customer_segments: List[CustomerSegmentationRequest] = Field(
        default_factory=list
    )

    note: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def validate_at_least_one_business_module(self):
        has_any_module = any(
            [
                self.sales_report is not None,
                self.voucher_fraud is not None,
                self.product_recommendation is not None,
                len(self.inventory_forecasts) > 0,
                len(self.customer_segments) > 0,
            ]
        )

        if not has_any_module:
            raise ValueError(
                "At least one business module data is required for review"
            )

        return self


class BusinessReviewModuleSummary(BaseModel):
    module_name: str
    summary: str
    risk_level: str
    risk_flags: List[str]
    recommendations: List[str]


class AICommerceBusinessReviewData(BaseModel):
    review_title: str
    overall_risk_level: str
    module_summaries: List[BusinessReviewModuleSummary]
    final_action_plan: List[str]
    provider: str
    model_name: str


class AICommerceBusinessReviewResponse(BaseModel):
    message: str
    data: AICommerceBusinessReviewData
