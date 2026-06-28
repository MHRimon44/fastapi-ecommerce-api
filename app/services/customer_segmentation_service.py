from app.providers.customer_segmentation_provider import customer_segmentation_provider
from app.schemas.customer_segmentation_schema import (
    CustomerSegmentationData,
    CustomerSegmentationRequest,
)


class CustomerSegmentationService:
    def segment_customer(
        self,
        request: CustomerSegmentationRequest,
    ) -> CustomerSegmentationData:
        return customer_segmentation_provider.segment_customer(request)


customer_segmentation_service = CustomerSegmentationService()
