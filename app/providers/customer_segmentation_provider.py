from typing import List

from app.core.config import settings
from app.schemas.customer_segmentation_schema import (
    CustomerSegmentationData,
    CustomerSegmentationRequest,
)


class MockCustomerSegmentationProvider:
    def segment_customer(
        self,
        request: CustomerSegmentationRequest,
    ) -> CustomerSegmentationData:
        score = 0
        insights: List[str] = []
        recommendations: List[str] = []
        risk_flags: List[str] = []

        score = self._score_purchase_value(request, score, insights)
        score = self._score_order_frequency(request, score, insights)
        score = self._score_recency(request, score, insights, risk_flags)
        score = self._score_return_and_cancel_behavior(
            request=request,
            score=score,
            insights=insights,
            risk_flags=risk_flags,
        )
        score = self._score_discount_behavior(
            request=request,
            score=score,
            insights=insights,
            risk_flags=risk_flags,
        )

        if score < 0:
            score = 0

        if score > 100:
            score = 100

        segment_name = self._get_segment_name(request, score)
        customer_value_level = self._get_customer_value_level(score)

        recommendations = self._build_recommendations(
            request=request,
            segment_name=segment_name,
            customer_value_level=customer_value_level,
            risk_flags=risk_flags,
        )

        if request.preferred_categories:
            insights.append(
                "Preferred categories: " + ", ".join(request.preferred_categories)
            )

        if request.preferred_channels:
            insights.append(
                "Preferred channels: " + ", ".join(request.preferred_channels)
            )

        if request.note:
            insights.append(f"Business note: {request.note}")

        return CustomerSegmentationData(
            segment_name=segment_name,
            segment_score=score,
            customer_value_level=customer_value_level,
            insights=insights,
            recommendations=recommendations,
            risk_flags=risk_flags,
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )

    def _score_purchase_value(
        self,
        request: CustomerSegmentationRequest,
        score: int,
        insights: List[str],
    ) -> int:
        if request.total_spent >= 100000:
            score += 35
            insights.append("Customer has very high lifetime spending.")

        elif request.total_spent >= 50000:
            score += 25
            insights.append("Customer has high lifetime spending.")

        elif request.total_spent >= 10000:
            score += 15
            insights.append("Customer has moderate lifetime spending.")

        else:
            score += 5
            insights.append("Customer has low lifetime spending.")

        if request.average_order_value >= 5000:
            score += 15
            insights.append("Average order value is strong.")

        elif request.average_order_value >= 2000:
            score += 10
            insights.append("Average order value is moderate.")

        return score

    def _score_order_frequency(
        self,
        request: CustomerSegmentationRequest,
        score: int,
        insights: List[str],
    ) -> int:
        if request.total_orders >= 20:
            score += 25
            insights.append("Customer has frequent purchase behavior.")

        elif request.total_orders >= 10:
            score += 18
            insights.append("Customer has repeat purchase behavior.")

        elif request.total_orders >= 3:
            score += 10
            insights.append("Customer has some repeat purchase behavior.")

        elif request.total_orders == 1:
            score += 3
            insights.append("Customer has only one order.")

        else:
            insights.append("Customer has no completed order history.")

        return score

    def _score_recency(
        self,
        request: CustomerSegmentationRequest,
        score: int,
        insights: List[str],
        risk_flags: List[str],
    ) -> int:
        if request.days_since_last_order is None:
            insights.append("Last order recency is not available.")
            return score

        if request.days_since_last_order <= 30:
            score += 20
            insights.append("Customer purchased recently.")

        elif request.days_since_last_order <= 90:
            score += 10
            insights.append("Customer purchased within the last 90 days.")

        elif request.days_since_last_order <= 180:
            score += 3
            insights.append("Customer is becoming inactive.")
            risk_flags.append("Customer has not purchased in more than 90 days.")

        else:
            score -= 10
            insights.append("Customer is inactive for a long period.")
            risk_flags.append("Customer is at high churn risk.")

        return score

    def _score_return_and_cancel_behavior(
        self,
        request: CustomerSegmentationRequest,
        score: int,
        insights: List[str],
        risk_flags: List[str],
    ) -> int:
        negative_order_count = request.return_order_count + request.cancelled_order_count

        if request.total_orders <= 0:
            return score

        negative_ratio = (negative_order_count / request.total_orders) * 100

        if negative_ratio >= 40:
            score -= 20
            risk_flags.append(
                f"High return/cancel ratio detected: {negative_ratio:.2f}%."
            )

        elif negative_ratio >= 20:
            score -= 10
            risk_flags.append(
                f"Return/cancel ratio needs review: {negative_ratio:.2f}%."
            )

        if negative_order_count > 0:
            insights.append(
                f"Return/cancel order count: {negative_order_count}."
            )

        return score

    def _score_discount_behavior(
        self,
        request: CustomerSegmentationRequest,
        score: int,
        insights: List[str],
        risk_flags: List[str],
    ) -> int:
        if request.total_orders <= 0:
            return score

        voucher_usage_ratio = (
            request.used_voucher_count / request.total_orders
        ) * 100

        if voucher_usage_ratio >= 70:
            score -= 10
            risk_flags.append(
                f"Customer is highly voucher-dependent: {voucher_usage_ratio:.2f}%."
            )

        elif voucher_usage_ratio >= 40:
            risk_flags.append(
                f"Customer often uses vouchers: {voucher_usage_ratio:.2f}%."
            )

        if request.used_voucher_count > 0:
            insights.append(
                f"Voucher used in {request.used_voucher_count} order(s)."
            )

        return score

    def _get_segment_name(
        self,
        request: CustomerSegmentationRequest,
        score: int,
    ) -> str:
        if request.total_orders == 0:
            return "NO_PURCHASE_CUSTOMER"

        if request.days_since_last_order is not None and request.days_since_last_order > 180:
            return "CHURN_RISK_CUSTOMER"

        if score >= 80:
            return "VIP_CUSTOMER"

        if score >= 60:
            return "LOYAL_CUSTOMER"

        if score >= 35:
            return "REGULAR_CUSTOMER"

        if request.total_orders == 1:
            return "NEW_CUSTOMER"

        return "LOW_VALUE_CUSTOMER"

    def _get_customer_value_level(
        self,
        score: int,
    ) -> str:
        if score >= 80:
            return "HIGH"

        if score >= 40:
            return "MEDIUM"

        return "LOW"

    def _build_recommendations(
        self,
        request: CustomerSegmentationRequest,
        segment_name: str,
        customer_value_level: str,
        risk_flags: List[str],
    ) -> List[str]:
        if segment_name == "VIP_CUSTOMER":
            return [
                "Offer early access to new products and premium campaigns.",
                "Protect this customer with priority support and personalized offers.",
                "Recommend high-value bundles based on preferred categories.",
            ]

        if segment_name == "LOYAL_CUSTOMER":
            return [
                "Send loyalty rewards or exclusive repeat-purchase offers.",
                "Recommend related products from preferred categories.",
                "Encourage higher basket value with bundle offers.",
            ]

        if segment_name == "CHURN_RISK_CUSTOMER":
            return [
                "Run win-back campaign with personalized offer.",
                "Ask for feedback to understand why the customer stopped purchasing.",
                "Send category-based recommendations from previous interests.",
            ]

        if segment_name == "NEW_CUSTOMER":
            return [
                "Send onboarding offer for second purchase.",
                "Recommend best-selling products from the same category.",
                "Use remarketing campaign within 7 to 14 days.",
            ]

        if segment_name == "NO_PURCHASE_CUSTOMER":
            return [
                "Send first-purchase campaign.",
                "Show entry-level products with strong value proposition.",
                "Track engagement before increasing campaign cost.",
            ]

        recommendations = [
            "Continue regular promotional communication.",
            "Recommend products based on preferred categories and previous behavior.",
        ]

        if customer_value_level == "LOW":
            recommendations.append(
                "Avoid high discount cost until customer purchase intent improves."
            )

        if risk_flags:
            recommendations.append(
                "Review risk flags before including customer in expensive campaigns."
            )

        return recommendations


customer_segmentation_provider = MockCustomerSegmentationProvider()
