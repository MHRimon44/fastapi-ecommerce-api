from typing import List, Optional

from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.business_ai_schema import (
    SalesReportAnalysisData,
    SalesReportAnalysisRequest,
    SalesChannelPerformance,
    TopProductPerformance,
)


class MockBusinessAIProvider:
    def analyze_sales_report(
        self,
        request: SalesReportAnalysisRequest,
    ) -> SalesReportAnalysisData:
        average_order_value = self._calculate_average_order_value(
            total_sales_amount=request.total_sales_amount,
            total_orders=request.total_orders,
        )

        sales_growth_percent = self._calculate_sales_growth_percent(
            current_sales=request.total_sales_amount,
            previous_sales=request.previous_sales_amount,
        )

        top_channel = self._get_top_channel(request.sales_channels)
        top_product = self._get_top_product(request.top_products)

        summary = self._build_summary(
            request=request,
            average_order_value=average_order_value,
            sales_growth_percent=sales_growth_percent,
            top_channel=top_channel,
            top_product=top_product,
        )

        insights = self._build_insights(
            request=request,
            average_order_value=average_order_value,
            sales_growth_percent=sales_growth_percent,
            top_channel=top_channel,
            top_product=top_product,
        )

        recommendations = self._build_recommendations(
            request=request,
            average_order_value=average_order_value,
            sales_growth_percent=sales_growth_percent,
            top_channel=top_channel,
            top_product=top_product,
        )

        risk_flags = self._build_risk_flags(
            request=request,
            sales_growth_percent=sales_growth_percent,
            top_product=top_product,
        )

        return SalesReportAnalysisData(
            summary=summary,
            average_order_value=round(average_order_value, 2),
            sales_growth_percent=sales_growth_percent,
            insights=insights,
            recommendations=recommendations,
            risk_flags=risk_flags,
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )

    def _calculate_average_order_value(
        self,
        total_sales_amount: float,
        total_orders: int,
    ) -> float:
        if total_orders <= 0:
            return 0

        return total_sales_amount / total_orders

    def _calculate_sales_growth_percent(
        self,
        current_sales: float,
        previous_sales: Optional[float],
    ) -> Optional[float]:
        if previous_sales is None:
            return None

        if previous_sales <= 0:
            return None

        growth = ((current_sales - previous_sales) / previous_sales) * 100

        return round(growth, 2)

    def _get_top_channel(
        self,
        channels: List[SalesChannelPerformance],
    ) -> Optional[SalesChannelPerformance]:
        if not channels:
            return None

        return max(
            channels,
            key=lambda item: item.sales_amount,
        )

    def _get_top_product(
        self,
        products: List[TopProductPerformance],
    ) -> Optional[TopProductPerformance]:
        if not products:
            return None

        return max(
            products,
            key=lambda item: item.sales_amount,
        )

    def _build_summary(
        self,
        request: SalesReportAnalysisRequest,
        average_order_value: float,
        sales_growth_percent: Optional[float],
        top_channel: Optional[SalesChannelPerformance],
        top_product: Optional[TopProductPerformance],
    ) -> str:
        summary = (
            f"{request.report_title}: Total sales amount is "
            f"{request.total_sales_amount:.2f} from {request.total_orders} orders. "
            f"Average order value is {average_order_value:.2f}."
        )

        if sales_growth_percent is not None:
            summary += f" Sales growth is {sales_growth_percent:.2f}% compared to previous period."

        if top_channel:
            summary += f" Top sales channel is {top_channel.channel_name}."

        if top_product:
            summary += f" Top product is {top_product.product_name}."

        return summary

    def _build_insights(
        self,
        request: SalesReportAnalysisRequest,
        average_order_value: float,
        sales_growth_percent: Optional[float],
        top_channel: Optional[SalesChannelPerformance],
        top_product: Optional[TopProductPerformance],
    ) -> List[str]:
        insights = [
            f"Total orders: {request.total_orders}",
            f"Total sales amount: {request.total_sales_amount:.2f}",
            f"Average order value: {average_order_value:.2f}",
            f"Total customers: {request.total_customers}",
            f"Total products sold: {request.total_products_sold}",
        ]

        if sales_growth_percent is not None:
            insights.append(f"Sales growth: {sales_growth_percent:.2f}%")

        if top_channel:
            insights.append(
                f"Best channel: {top_channel.channel_name} with sales {top_channel.sales_amount:.2f}"
            )

        if top_product:
            insights.append(
                f"Best product: {top_product.product_name} with sales {top_product.sales_amount:.2f}"
            )

        if request.note:
            insights.append(f"Business note: {request.note}")

        return insights

    def _build_recommendations(
        self,
        request: SalesReportAnalysisRequest,
        average_order_value: float,
        sales_growth_percent: Optional[float],
        top_channel: Optional[SalesChannelPerformance],
        top_product: Optional[TopProductPerformance],
    ) -> List[str]:
        recommendations: List[str] = []

        if request.total_orders == 0:
            recommendations.append(
                "No orders found. Review marketing campaigns, product visibility, and checkout issues."
            )
            return recommendations

        if sales_growth_percent is not None and sales_growth_percent < 0:
            recommendations.append(
                "Sales declined compared to the previous period. Review pricing, campaigns, stock availability, and channel performance."
            )

        if average_order_value > 0:
            recommendations.append(
                "Use bundle offers or cross-sell campaigns to increase average order value."
            )

        if top_channel:
            recommendations.append(
                f"Increase focus on {top_channel.channel_name}, because it is currently the strongest sales channel."
            )

        if top_product:
            recommendations.append(
                f"Maintain stock and promotion for {top_product.product_name}, because it is the top-performing product."
            )

        if not recommendations:
            recommendations.append(
                "Continue monitoring sales trends, top products, and channel-wise performance."
            )

        return recommendations

    def _build_risk_flags(
        self,
        request: SalesReportAnalysisRequest,
        sales_growth_percent: Optional[float],
        top_product: Optional[TopProductPerformance],
    ) -> List[str]:
        risk_flags: List[str] = []

        if request.total_sales_amount == 0:
            risk_flags.append("No sales amount recorded for this report.")

        if request.total_orders == 0:
            risk_flags.append("No orders recorded for this report.")

        if sales_growth_percent is not None and sales_growth_percent < 0:
            risk_flags.append("Sales dropped compared to the previous period.")

        if top_product and request.total_sales_amount > 0:
            contribution_percent = (
                top_product.sales_amount / request.total_sales_amount
            ) * 100

            if contribution_percent >= 50:
                risk_flags.append(
                    f"High dependency on one product: {top_product.product_name} contributes {contribution_percent:.2f}% of sales."
                )

        return risk_flags


def get_business_ai_provider():
    if settings.AI_PROVIDER == "mock":
        return MockBusinessAIProvider()

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unsupported business AI provider",
    )
