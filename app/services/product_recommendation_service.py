from app.providers.product_recommendation_provider import (
    product_recommendation_provider,
)
from app.schemas.product_recommendation_schema import (
    ProductRecommendationData,
    ProductRecommendationRequest,
)


class ProductRecommendationService:
    def recommend_products(
        self,
        request: ProductRecommendationRequest,
    ) -> ProductRecommendationData:
        return product_recommendation_provider.recommend_products(request)


product_recommendation_service = ProductRecommendationService()
