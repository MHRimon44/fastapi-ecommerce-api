import math
from typing import List, Optional

from app.core.config import settings
from app.schemas.inventory_demand_schema import (
    InventoryDemandForecastData,
    InventoryDemandForecastRequest,
)


class MockInventoryDemandProvider:
    def forecast_demand(
        self,
        request: InventoryDemandForecastRequest,
    ) -> InventoryDemandForecastData:
        average_daily_sales = self._calculate_average_daily_sales(request)
        forecasted_demand_qty = math.ceil(
            average_daily_sales * request.forecast_days
        )

        available_stock_qty = request.current_stock_qty + request.incoming_stock_qty

        estimated_stock_remaining_days = self._calculate_stock_remaining_days(
            available_stock_qty=available_stock_qty,
            average_daily_sales=average_daily_sales,
        )

        reorder_needed = self._is_reorder_needed(
            request=request,
            available_stock_qty=available_stock_qty,
            forecasted_demand_qty=forecasted_demand_qty,
        )

        suggested_reorder_qty = self._calculate_suggested_reorder_qty(
            request=request,
            available_stock_qty=available_stock_qty,
            forecasted_demand_qty=forecasted_demand_qty,
        )

        risk_level = self._get_risk_level(
            request=request,
            available_stock_qty=available_stock_qty,
            average_daily_sales=average_daily_sales,
            estimated_stock_remaining_days=estimated_stock_remaining_days,
            reorder_needed=reorder_needed,
        )

        insights = self._build_insights(
            request=request,
            average_daily_sales=average_daily_sales,
            forecasted_demand_qty=forecasted_demand_qty,
            available_stock_qty=available_stock_qty,
            estimated_stock_remaining_days=estimated_stock_remaining_days,
        )

        recommendations = self._build_recommendations(
            request=request,
            reorder_needed=reorder_needed,
            suggested_reorder_qty=suggested_reorder_qty,
            risk_level=risk_level,
            estimated_stock_remaining_days=estimated_stock_remaining_days,
        )

        return InventoryDemandForecastData(
            product_name=request.product_name,
            average_daily_sales=round(average_daily_sales, 2),
            forecasted_demand_qty=forecasted_demand_qty,
            available_stock_qty=available_stock_qty,
            estimated_stock_remaining_days=estimated_stock_remaining_days,
            reorder_needed=reorder_needed,
            suggested_reorder_qty=suggested_reorder_qty,
            risk_level=risk_level,
            insights=insights,
            recommendations=recommendations,
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )

    def _calculate_average_daily_sales(
        self,
        request: InventoryDemandForecastRequest,
    ) -> float:
        total_quantity_sold = sum(
            item.quantity_sold
            for item in request.sales_history
        )

        history_period_count = len(request.sales_history)

        if history_period_count <= 0:
            return 0

        return total_quantity_sold / history_period_count

    def _calculate_stock_remaining_days(
        self,
        available_stock_qty: int,
        average_daily_sales: float,
    ) -> Optional[float]:
        if average_daily_sales <= 0:
            return None

        return round(available_stock_qty / average_daily_sales, 2)

    def _is_reorder_needed(
        self,
        request: InventoryDemandForecastRequest,
        available_stock_qty: int,
        forecasted_demand_qty: int,
    ) -> bool:
        if available_stock_qty <= request.reorder_point:
            return True

        required_stock = forecasted_demand_qty + request.safety_stock_qty

        return available_stock_qty < required_stock

    def _calculate_suggested_reorder_qty(
        self,
        request: InventoryDemandForecastRequest,
        available_stock_qty: int,
        forecasted_demand_qty: int,
    ) -> int:
        required_stock = forecasted_demand_qty + request.safety_stock_qty

        shortage_qty = required_stock - available_stock_qty

        if shortage_qty <= 0:
            return 0

        return shortage_qty

    def _get_risk_level(
        self,
        request: InventoryDemandForecastRequest,
        available_stock_qty: int,
        average_daily_sales: float,
        estimated_stock_remaining_days: Optional[float],
        reorder_needed: bool,
    ) -> str:
        if available_stock_qty == 0:
            return "HIGH"

        if estimated_stock_remaining_days is not None:
            if estimated_stock_remaining_days <= request.lead_time_days:
                return "HIGH"

            if estimated_stock_remaining_days <= request.lead_time_days + 7:
                return "MEDIUM"

        if reorder_needed:
            return "MEDIUM"

        if average_daily_sales == 0:
            return "LOW"

        return "LOW"

    def _build_insights(
        self,
        request: InventoryDemandForecastRequest,
        average_daily_sales: float,
        forecasted_demand_qty: int,
        available_stock_qty: int,
        estimated_stock_remaining_days: Optional[float],
    ) -> List[str]:
        insights = [
            f"Average daily sales: {average_daily_sales:.2f}",
            f"Forecasted demand for {request.forecast_days} days: {forecasted_demand_qty}",
            f"Available stock including incoming stock: {available_stock_qty}",
            f"Reorder point: {request.reorder_point}",
            f"Safety stock: {request.safety_stock_qty}",
        ]

        if estimated_stock_remaining_days is None:
            insights.append("Stock remaining days cannot be calculated because average sales is zero.")
        else:
            insights.append(
                f"Estimated stock remaining days: {estimated_stock_remaining_days:.2f}"
            )

        if request.note:
            insights.append(f"Business note: {request.note}")

        return insights

    def _build_recommendations(
        self,
        request: InventoryDemandForecastRequest,
        reorder_needed: bool,
        suggested_reorder_qty: int,
        risk_level: str,
        estimated_stock_remaining_days: Optional[float],
    ) -> List[str]:
        recommendations: List[str] = []

        if reorder_needed:
            recommendations.append(
                f"Create purchase/replenishment request for at least {suggested_reorder_qty} units."
            )

        if risk_level == "HIGH":
            recommendations.append(
                "Prioritize replenishment because stock-out risk is high."
            )

        if estimated_stock_remaining_days is not None:
            if estimated_stock_remaining_days <= request.lead_time_days:
                recommendations.append(
                    "Stock may run out before supplier lead time ends."
                )

        if not reorder_needed:
            recommendations.append(
                "Current stock is sufficient for the selected forecast period."
            )

        recommendations.append(
            "Review demand weekly and update forecast with latest sales data."
        )

        return recommendations


inventory_demand_provider = MockInventoryDemandProvider()
