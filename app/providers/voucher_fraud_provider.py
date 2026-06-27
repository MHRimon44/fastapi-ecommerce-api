from typing import List

from app.core.config import settings
from app.schemas.voucher_fraud_schema import (
    CustomerVoucherUsagePattern,
    VoucherFraudDetectData,
    VoucherFraudDetectRequest,
)


class MockVoucherFraudProvider:
    def detect_fraud(
        self,
        request: VoucherFraudDetectRequest,
    ) -> VoucherFraudDetectData:
        risk_score = 0
        signals: List[str] = []
        recommendations: List[str] = []

        risk_score = self._check_usage_limit(
            request=request,
            current_score=risk_score,
            signals=signals,
        )

        risk_score = self._check_discount_ratio(
            request=request,
            current_score=risk_score,
            signals=signals,
        )

        risk_score = self._check_repeated_customer_usage(
            request=request,
            current_score=risk_score,
            signals=signals,
        )

        risk_score = self._check_suspicious_orders(
            request=request,
            current_score=risk_score,
            signals=signals,
        )

        risk_score = self._check_customer_patterns(
            customer_patterns=request.customer_patterns,
            current_score=risk_score,
            signals=signals,
        )

        if risk_score > 100:
            risk_score = 100

        risk_level = self._get_risk_level(risk_score)

        is_suspicious = risk_level in ["MEDIUM", "HIGH"]

        recommendations = self._build_recommendations(
            risk_level=risk_level,
            signals=signals,
        )

        return VoucherFraudDetectData(
            risk_score=risk_score,
            risk_level=risk_level,
            is_suspicious=is_suspicious,
            signals=signals,
            recommendations=recommendations,
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )

    def _check_usage_limit(
        self,
        request: VoucherFraudDetectRequest,
        current_score: int,
        signals: List[str],
    ) -> int:
        if request.usage_limit is None:
            return current_score

        if request.usage_limit == 0:
            return current_score

        usage_percent = (request.used_count / request.usage_limit) * 100

        if usage_percent >= 100:
            signals.append("Voucher usage limit has been fully consumed.")
            current_score += 25

        elif usage_percent >= 80:
            signals.append("Voucher usage is above 80% of the usage limit.")
            current_score += 15

        return current_score

    def _check_discount_ratio(
        self,
        request: VoucherFraudDetectRequest,
        current_score: int,
        signals: List[str],
    ) -> int:
        if request.total_sales_amount <= 0:
            return current_score

        discount_ratio = (
            request.total_discount_given / request.total_sales_amount
        ) * 100

        if discount_ratio >= 40:
            signals.append(
                f"Total discount is very high compared to sales: {discount_ratio:.2f}%."
            )
            current_score += 30

        elif discount_ratio >= 25:
            signals.append(
                f"Total discount is high compared to sales: {discount_ratio:.2f}%."
            )
            current_score += 20

        return current_score

    def _check_repeated_customer_usage(
        self,
        request: VoucherFraudDetectRequest,
        current_score: int,
        signals: List[str],
    ) -> int:
        if request.total_orders_using_voucher <= 0:
            return current_score

        repeated_usage_ratio = (
            request.repeated_customers_count / request.total_orders_using_voucher
        ) * 100

        if repeated_usage_ratio >= 50:
            signals.append(
                f"Repeated customer usage is high: {repeated_usage_ratio:.2f}%."
            )
            current_score += 25

        elif repeated_usage_ratio >= 30:
            signals.append(
                f"Repeated customer usage needs review: {repeated_usage_ratio:.2f}%."
            )
            current_score += 15

        return current_score

    def _check_suspicious_orders(
        self,
        request: VoucherFraudDetectRequest,
        current_score: int,
        signals: List[str],
    ) -> int:
        if request.suspicious_order_count <= 0:
            return current_score

        signals.append(
            f"{request.suspicious_order_count} suspicious orders detected using this voucher."
        )

        current_score += min(
            request.suspicious_order_count * 10,
            30,
        )

        return current_score

    def _check_customer_patterns(
        self,
        customer_patterns: List[CustomerVoucherUsagePattern],
        current_score: int,
        signals: List[str],
    ) -> int:
        for pattern in customer_patterns:
            if pattern.usage_count >= 5:
                label = pattern.customer_name or f"Customer {pattern.customer_id}"
                signals.append(
                    f"{label} used the voucher {pattern.usage_count} times."
                )
                current_score += 15

            if pattern.total_order_amount > 0:
                discount_ratio = (
                    pattern.total_discount_amount / pattern.total_order_amount
                ) * 100

                if discount_ratio >= 50:
                    label = pattern.customer_name or f"Customer {pattern.customer_id}"
                    signals.append(
                        f"{label} received very high discount ratio: {discount_ratio:.2f}%."
                    )
                    current_score += 15

        return current_score

    def _get_risk_level(
        self,
        risk_score: int,
    ) -> str:
        if risk_score >= 70:
            return "HIGH"

        if risk_score >= 35:
            return "MEDIUM"

        return "LOW"

    def _build_recommendations(
        self,
        risk_level: str,
        signals: List[str],
    ) -> List[str]:
        if risk_level == "HIGH":
            return [
                "Temporarily disable the voucher and review usage history.",
                "Check repeated customers, suspicious orders, and abnormal discount patterns.",
                "Add stricter per-customer usage limit and minimum purchase rule.",
            ]

        if risk_level == "MEDIUM":
            return [
                "Review voucher usage before allowing further campaign scaling.",
                "Monitor customers with repeated voucher usage.",
                "Consider limiting voucher usage per customer.",
            ]

        return [
            "Voucher usage looks normal based on current data.",
            "Continue monitoring usage limit, repeated users, and discount ratio.",
        ]


voucher_fraud_provider = MockVoucherFraudProvider()
