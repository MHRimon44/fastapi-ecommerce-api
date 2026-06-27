from fastapi import APIRouter, status

from app.schemas.business_ai_schema import (
    SalesReportAnalysisRequest,
    SalesReportAnalysisResponse,
)
from app.schemas.inventory_demand_schema import (
    InventoryDemandForecastRequest,
    InventoryDemandForecastResponse,
)
from app.schemas.product_recommendation_schema import (
    ProductRecommendationRequest,
    ProductRecommendationResponse,
)
from app.schemas.voucher_fraud_schema import (
    VoucherFraudDetectRequest,
    VoucherFraudDetectResponse,
)
from app.services.business_ai_service import business_ai_service
from app.services.inventory_demand_service import inventory_demand_service
from app.services.product_recommendation_service import product_recommendation_service
from app.services.voucher_fraud_service import voucher_fraud_service


router = APIRouter(
    prefix="/business-ai",
    tags=["Business AI"],
)


@router.post(
    "/sales-report/analyze",
    response_model=SalesReportAnalysisResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_sales_report(
    request: SalesReportAnalysisRequest,
) -> SalesReportAnalysisResponse:
    data = business_ai_service.analyze_sales_report(request)

    return SalesReportAnalysisResponse(
        message="Sales report analyzed successfully",
        data=data,
    )


@router.post(
    "/voucher-fraud/detect",
    response_model=VoucherFraudDetectResponse,
    status_code=status.HTTP_200_OK,
)
def detect_voucher_fraud(
    request: VoucherFraudDetectRequest,
) -> VoucherFraudDetectResponse:
    data = voucher_fraud_service.detect_fraud(request)

    return VoucherFraudDetectResponse(
        message="Voucher fraud risk analyzed successfully",
        data=data,
    )


@router.post(
    "/product-recommendations/recommend",
    response_model=ProductRecommendationResponse,
    status_code=status.HTTP_200_OK,
)
def recommend_products(
    request: ProductRecommendationRequest,
) -> ProductRecommendationResponse:
    data = product_recommendation_service.recommend_products(request)

    return ProductRecommendationResponse(
        message="Product recommendations generated successfully",
        data=data,
    )


@router.post(
    "/inventory-demand/forecast",
    response_model=InventoryDemandForecastResponse,
    status_code=status.HTTP_200_OK,
)
def forecast_inventory_demand(
    request: InventoryDemandForecastRequest,
) -> InventoryDemandForecastResponse:
    data = inventory_demand_service.forecast_demand(request)

    return InventoryDemandForecastResponse(
        message="Inventory demand forecast generated successfully",
        data=data,
    )
