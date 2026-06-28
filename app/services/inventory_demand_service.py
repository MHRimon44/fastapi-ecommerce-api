from app.providers.inventory_demand_provider import inventory_demand_provider
from app.schemas.inventory_demand_schema import (
    InventoryDemandForecastData,
    InventoryDemandForecastRequest,
)


class InventoryDemandService:
    def forecast_demand(
        self,
        request: InventoryDemandForecastRequest,
    ) -> InventoryDemandForecastData:
        return inventory_demand_provider.forecast_demand(request)


inventory_demand_service = InventoryDemandService()
