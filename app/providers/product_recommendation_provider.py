from typing import List

from app.core.config import settings
from app.schemas.product_recommendation_schema import (
    ProductCandidate,
    ProductRecommendationData,
    ProductRecommendationRequest,
    RecommendedProduct,
)


class MockProductRecommendationProvider:
    def recommend_products(
        self,
        request: ProductRecommendationRequest,
    ) -> ProductRecommendationData:
        scored_products: List[RecommendedProduct] = []

        for product in request.products:
            if product.stock_qty <= 0:
                continue

            score = 0
            reasons: List[str] = []

            score = self._score_category_match(
                product=product,
                request=request,
                score=score,
                reasons=reasons,
            )

            score = self._score_feature_match(
                product=product,
                request=request,
                score=score,
                reasons=reasons,
            )

            score = self._score_budget_match(
                product=product,
                request=request,
                score=score,
                reasons=reasons,
            )

            score = self._score_use_case_match(
                product=product,
                request=request,
                score=score,
                reasons=reasons,
            )

            score = self._score_popularity(
                product=product,
                score=score,
                reasons=reasons,
            )

            if not reasons:
                reasons.append("Product is available in stock.")

            scored_products.append(
                RecommendedProduct(
                    product_id=product.product_id,
                    product_name=product.product_name,
                    sku=product.sku,
                    category=product.category,
                    price=product.price,
                    stock_qty=product.stock_qty,
                    recommendation_score=min(score, 100),
                    reasons=reasons,
                )
            )

        scored_products.sort(
            key=lambda item: item.recommendation_score,
            reverse=True,
        )

        recommended_products = scored_products[: request.top_k]

        summary = self._build_summary(
            request=request,
            recommended_products=recommended_products,
        )

        return ProductRecommendationData(
            recommended_products=recommended_products,
            summary=summary,
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )

    def _score_category_match(
        self,
        product: ProductCandidate,
        request: ProductRecommendationRequest,
        score: int,
        reasons: List[str],
    ) -> int:
        product_category = (product.category or "").lower()

        preferred_categories = [
            category.lower()
            for category in request.preferred_categories
        ]

        previous_categories = [
            category.lower()
            for category in request.previous_purchase_categories
        ]

        if product_category and product_category in preferred_categories:
            score += 30
            reasons.append("Matches preferred category.")

        if product_category and product_category in previous_categories:
            score += 15
            reasons.append("Similar to previous purchase category.")

        return score

    def _score_feature_match(
        self,
        product: ProductCandidate,
        request: ProductRecommendationRequest,
        score: int,
        reasons: List[str],
    ) -> int:
        product_text = self._product_search_text(product)

        matched_features = []

        for feature in request.preferred_features:
            if feature.lower() in product_text:
                matched_features.append(feature)

        if matched_features:
            score += min(len(matched_features) * 10, 30)
            reasons.append(
                "Matches preferred features: " + ", ".join(matched_features)
            )

        return score

    def _score_budget_match(
        self,
        product: ProductCandidate,
        request: ProductRecommendationRequest,
        score: int,
        reasons: List[str],
    ) -> int:
        if request.budget_min is not None and product.price < request.budget_min:
            return score

        if request.budget_max is not None and product.price > request.budget_max:
            return score

        if request.budget_min is not None or request.budget_max is not None:
            score += 20
            reasons.append("Fits customer budget range.")

        return score

    def _score_use_case_match(
        self,
        product: ProductCandidate,
        request: ProductRecommendationRequest,
        score: int,
        reasons: List[str],
    ) -> int:
        if not request.use_case:
            return score

        use_case_words = request.use_case.lower().split()
        product_text = self._product_search_text(product)

        matched_words = [
            word
            for word in use_case_words
            if word in product_text
        ]

        if matched_words:
            score += min(len(matched_words) * 5, 20)
            reasons.append("Matches customer use case.")

        return score

    def _score_popularity(
        self,
        product: ProductCandidate,
        score: int,
        reasons: List[str],
    ) -> int:
        if product.rating is not None and product.rating >= 4.5:
            score += 10
            reasons.append("Highly rated product.")

        if product.sales_count is not None and product.sales_count >= 50:
            score += 10
            reasons.append("Popular product based on sales history.")

        return score

    def _product_search_text(
        self,
        product: ProductCandidate,
    ) -> str:
        values = [
            product.product_name,
            product.category or "",
            product.description or "",
            " ".join(product.features),
            " ".join(product.tags),
        ]

        return " ".join(values).lower()

    def _build_summary(
        self,
        request: ProductRecommendationRequest,
        recommended_products: List[RecommendedProduct],
    ) -> str:
        if not recommended_products:
            return "No suitable products found based on the given preferences."

        top_product = recommended_products[0]

        return (
            f"Recommended {len(recommended_products)} product(s). "
            f"Top recommendation is {top_product.product_name} with score "
            f"{top_product.recommendation_score}."
        )


product_recommendation_provider = MockProductRecommendationProvider()
