from typing import List

from app.core.config import settings
from app.schemas.ai_commerce_schema import (
    AICommerceBusinessReviewData,
    AICommerceBusinessReviewRequest,
    BusinessReviewModuleSummary,
)
from app.services.business_ai_service import business_ai_service
from app.services.customer_segmentation_service import customer_segmentation_service
from app.services.inventory_demand_service import inventory_demand_service
from app.services.product_recommendation_service import product_recommendation_service
from app.services.voucher_fraud_service import voucher_fraud_service


class AICommerceService:
    def create_business_review(
        self,
        request: AICommerceBusinessReviewRequest,
    ) -> AICommerceBusinessReviewData:
        module_summaries: List[BusinessReviewModuleSummary] = []

        if request.sales_report:
            module_summaries.append(
                self._analyze_sales_report(request)
            )

        if request.voucher_fraud:
            module_summaries.append(
                self._analyze_voucher_fraud(request)
            )

        if request.product_recommendation:
            module_summaries.append(
                self._analyze_product_recommendation(request)
            )

        if request.inventory_forecasts:
            module_summaries.append(
                self._analyze_inventory_forecasts(request)
            )

        if request.customer_segments:
            module_summaries.append(
                self._analyze_customer_segments(request)
            )

        overall_risk_level = self._get_overall_risk_level(module_summaries)

        final_action_plan = self._build_final_action_plan(
            module_summaries=module_summaries,
            overall_risk_level=overall_risk_level,
        )

        if request.note:
            final_action_plan.append(
                f"Review business note: {request.note}"
            )

        return AICommerceBusinessReviewData(
            review_title=request.review_title,
            overall_risk_level=overall_risk_level,
            module_summaries=module_summaries,
            final_action_plan=self._unique_items(final_action_plan)[:10],
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )

    def _analyze_sales_report(
        self,
        request: AICommerceBusinessReviewRequest,
    ) -> BusinessReviewModuleSummary:
        data = business_ai_service.analyze_sales_report(request.sales_report)

        risk_level = "LOW"

        if data.risk_flags:
            risk_level = "MEDIUM"

        if data.sales_growth_percent is not None and data.sales_growth_percent < 0:
            risk_level = "HIGH"

        if "No orders recorded for this report." in data.risk_flags:
            risk_level = "HIGH"

        return BusinessReviewModuleSummary(
            module_name="Sales Report",
            summary=data.summary,
            risk_level=risk_level,
            risk_flags=data.risk_flags,
            recommendations=data.recommendations,
        )

    def _analyze_voucher_fraud(
        self,
        request: AICommerceBusinessReviewRequest,
    ) -> BusinessReviewModuleSummary:
        data = voucher_fraud_service.detect_fraud(request.voucher_fraud)

        return BusinessReviewModuleSummary(
            module_name="Voucher Fraud",
            summary=(
                f"Voucher fraud risk level is {data.risk_level} "
                f"with risk score {data.risk_score}."
            ),
            risk_level=data.risk_level,
            risk_flags=data.signals,
            recommendations=data.recommendations,
        )

    def _analyze_product_recommendation(
        self,
        request: AICommerceBusinessReviewRequest,
    ) -> BusinessReviewModuleSummary:
        data = product_recommendation_service.recommend_products(
            request.product_recommendation
        )

        risk_level = "LOW"

        if not data.recommended_products:
            risk_level = "MEDIUM"

        recommendations: List[str] = []

        for product in data.recommended_products:
            recommendations.append(
                f"Promote {product.product_name} because recommendation score is {product.recommendation_score}."
            )

        if not recommendations:
            recommendations.append(
                "No product recommendation found. Review product stock, price, and customer preference data."
            )

        return BusinessReviewModuleSummary(
            module_name="Product Recommendation",
            summary=data.summary,
            risk_level=risk_level,
            risk_flags=[] if data.recommended_products else ["No suitable recommended product found."],
            recommendations=recommendations,
        )

    def _analyze_inventory_forecasts(
        self,
        request: AICommerceBusinessReviewRequest,
    ) -> BusinessReviewModuleSummary:
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0

        risk_flags: List[str] = []
        recommendations: List[str] = []

        for forecast_request in request.inventory_forecasts:
            data = inventory_demand_service.forecast_demand(forecast_request)

            if data.risk_level == "HIGH":
                high_risk_count += 1
            elif data.risk_level == "MEDIUM":
                medium_risk_count += 1
            else:
                low_risk_count += 1

            if data.reorder_needed:
                risk_flags.append(
                    f"{data.product_name} needs reorder. Suggested reorder quantity: {data.suggested_reorder_qty}."
                )

            recommendations.extend(data.recommendations)

        risk_level = "LOW"

        if high_risk_count > 0:
            risk_level = "HIGH"
        elif medium_risk_count > 0:
            risk_level = "MEDIUM"

        summary = (
            f"Inventory forecast completed for {len(request.inventory_forecasts)} product(s). "
            f"HIGH risk: {high_risk_count}, MEDIUM risk: {medium_risk_count}, LOW risk: {low_risk_count}."
        )

        return BusinessReviewModuleSummary(
            module_name="Inventory Demand",
            summary=summary,
            risk_level=risk_level,
            risk_flags=self._unique_items(risk_flags),
            recommendations=self._unique_items(recommendations),
        )

    def _analyze_customer_segments(
        self,
        request: AICommerceBusinessReviewRequest,
    ) -> BusinessReviewModuleSummary:
        vip_count = 0
        loyal_count = 0
        churn_risk_count = 0
        no_purchase_count = 0

        risk_flags: List[str] = []
        recommendations: List[str] = []

        for segment_request in request.customer_segments:
            data = customer_segmentation_service.segment_customer(segment_request)

            if data.segment_name == "VIP_CUSTOMER":
                vip_count += 1

            if data.segment_name == "LOYAL_CUSTOMER":
                loyal_count += 1

            if data.segment_name == "CHURN_RISK_CUSTOMER":
                churn_risk_count += 1

            if data.segment_name == "NO_PURCHASE_CUSTOMER":
                no_purchase_count += 1

            risk_flags.extend(data.risk_flags)
            recommendations.extend(data.recommendations)

        risk_level = "LOW"

        if churn_risk_count > 0:
            risk_level = "HIGH"
        elif no_purchase_count > 0:
            risk_level = "MEDIUM"

        summary = (
            f"Customer segmentation completed for {len(request.customer_segments)} customer(s). "
            f"VIP: {vip_count}, Loyal: {loyal_count}, Churn Risk: {churn_risk_count}, No Purchase: {no_purchase_count}."
        )

        return BusinessReviewModuleSummary(
            module_name="Customer Segmentation",
            summary=summary,
            risk_level=risk_level,
            risk_flags=self._unique_items(risk_flags),
            recommendations=self._unique_items(recommendations),
        )

    def _get_overall_risk_level(
        self,
        module_summaries: List[BusinessReviewModuleSummary],
    ) -> str:
        risk_priority = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
        }

        highest = "LOW"

        for item in module_summaries:
            if risk_priority[item.risk_level] > risk_priority[highest]:
                highest = item.risk_level

        return highest

    def _build_final_action_plan(
        self,
        module_summaries: List[BusinessReviewModuleSummary],
        overall_risk_level: str,
    ) -> List[str]:
        action_plan: List[str] = []

        if overall_risk_level == "HIGH":
            action_plan.append(
                "Prioritize high-risk issues before scaling campaigns or promotions."
            )

        elif overall_risk_level == "MEDIUM":
            action_plan.append(
                "Review medium-risk areas and monitor them before making major business decisions."
            )

        else:
            action_plan.append(
                "Business signals look stable. Continue monitoring sales, stock, customer, and voucher performance."
            )

        for module_summary in module_summaries:
            for recommendation in module_summary.recommendations[:2]:
                action_plan.append(
                    f"{module_summary.module_name}: {recommendation}"
                )

        return action_plan

    def _unique_items(
        self,
        items: List[str],
    ) -> List[str]:
        result: List[str] = []

        for item in items:
            if item not in result:
                result.append(item)

        return result


ai_commerce_service = AICommerceService()
