from typing import Any, Dict, Type, get_origin

from pydantic import BaseModel

from app.core.config import settings
from app.providers.ollama_provider import ollama_provider
from app.schemas.ai_schema import (
    CustomerSupportReplyData,
    CustomerSupportReplyRequest,
    GenerateProductDescriptionRequest,
    OrderReportSummaryData,
    ProductDescriptionData,
    SummarizeOrderReportRequest,
)


def _safe_get(obj: Any, name: str, default: Any = None) -> Any:
    return getattr(obj, name, default)


def _build_pydantic_model(
    model_class: Type[BaseModel],
    values: Dict[str, Any],
) -> BaseModel:
    """
    Builds response model safely even if schema field names are different.
    Important: list fields must receive list values, not empty string.
    """
    final_values = {}

    fields = getattr(model_class, "model_fields", {})

    for field_name, field_info in fields.items():
        if field_name in values:
            final_values[field_name] = values[field_name]
            continue

        lower_name = field_name.lower()
        annotation = field_info.annotation
        origin = get_origin(annotation)

        if origin is list or annotation is list:
            if "action" in lower_name:
                final_values[field_name] = [
                    "Review the AI response",
                    "Use the response after business verification",
                ]
            elif "recommendation" in lower_name:
                final_values[field_name] = [
                    "Review the summary",
                    "Take action based on business priority",
                ]
            elif "insight" in lower_name:
                final_values[field_name] = [
                    "AI-generated insight should be reviewed by admin",
                ]
            else:
                final_values[field_name] = []
        elif "description" in lower_name:
            final_values[field_name] = values.get("content", "")
        elif "summary" in lower_name:
            final_values[field_name] = values.get("content", "")
        elif "reply" in lower_name:
            final_values[field_name] = values.get("content", "")
        elif "provider" in lower_name:
            final_values[field_name] = values.get("provider", settings.AI_PROVIDER)
        elif "model" in lower_name:
            final_values[field_name] = values.get("model_name", settings.AI_MODEL_NAME)
        elif "product_name" in lower_name:
            final_values[field_name] = values.get("product_name", "")
        elif "category" in lower_name:
            final_values[field_name] = values.get("category", "")
        elif "report_title" in lower_name:
            final_values[field_name] = values.get("report_title", "")
        elif "order_status" in lower_name:
            final_values[field_name] = values.get("order_status", "")
        else:
            if annotation is int:
                final_values[field_name] = 0
            elif annotation is float:
                final_values[field_name] = 0.0
            elif annotation is bool:
                final_values[field_name] = False
            else:
                final_values[field_name] = ""

    return model_class(**final_values)


class MockAIProvider:
    def generate_product_description(
        self,
        request: GenerateProductDescriptionRequest,
    ) -> ProductDescriptionData:
        product_name = _safe_get(request, "product_name", "")
        category = _safe_get(request, "category", "")
        features = _safe_get(request, "features", [])
        tone = _safe_get(request, "tone", "Professional")

        content = (
            f"{product_name} is a {tone.lower()} {category.lower()} product "
            f"designed with {', '.join(features)}. It is suitable for customers "
            f"who want quality, comfort, and daily usability."
        )

        return _build_pydantic_model(
            ProductDescriptionData,
            {
                "content": content,
                "description": content,
                "product_description": content,
                "product_name": product_name,
                "category": category,
                "provider": "mock",
                "model_name": settings.AI_MODEL_NAME,
                "keywords": ["quality", "comfort", "daily use"],
                "seo_keywords": ["quality", "comfort", "daily use"],
                "bullet_points": [
                    "Built for daily use",
                    "Designed for comfort",
                    "Suitable for e-commerce customers",
                ],
            },
        )

    def summarize_order_report(
        self,
        request: SummarizeOrderReportRequest,
    ) -> OrderReportSummaryData:
        report_title = _safe_get(request, "report_title", "")
        total_orders = _safe_get(request, "total_orders", 0)
        total_sales_amount = _safe_get(request, "total_sales_amount", 0)
        total_customers = _safe_get(request, "total_customers", 0)

        content = (
            f"{report_title}: Total orders were {total_orders}, total sales amount "
            f"was {total_sales_amount}, and total customers were {total_customers}. "
            f"Top products indicate the main sales drivers."
        )

        return _build_pydantic_model(
            OrderReportSummaryData,
            {
                "content": content,
                "summary": content,
                "report_title": report_title,
                "provider": "mock",
                "model_name": settings.AI_MODEL_NAME,
                "insights": [
                    "Total order volume should be monitored regularly",
                    "Top products are the main sales drivers",
                    "Customer count shows current market reach",
                ],
                "recommendations": [
                    "Promote top-selling products",
                    "Review low-performing products",
                    "Track sales trend by channel",
                ],
                "key_insights": [
                    "Total order volume should be monitored regularly",
                    "Top products are the main sales drivers",
                    "Customer count shows current market reach",
                ],
            },
        )

    def generate_customer_support_reply(
        self,
        request: CustomerSupportReplyRequest,
    ) -> CustomerSupportReplyData:
        customer_name = _safe_get(request, "customer_name", "customer")
        order_no = _safe_get(request, "order_no", "")
        customer_message = _safe_get(request, "customer_message", "")
        order_status = _safe_get(request, "order_status", "")
        tone = _safe_get(request, "tone", "Professional")

        content = (
            f"Dear {customer_name}, thank you for contacting us about order {order_no}. "
            f"We received your message: {customer_message} "
            f"Your order status is {order_status or 'being checked'}. "
            f"Our team will assist you as soon as possible."
        )

        return _build_pydantic_model(
            CustomerSupportReplyData,
            {
                "content": content,
                "reply": content,
                "customer_name": customer_name,
                "order_no": order_no,
                "order_status": order_status,
                "tone": tone,
                "provider": "mock",
                "model_name": settings.AI_MODEL_NAME,
                "suggested_actions": [
                    "Check courier tracking",
                    "Verify order status",
                    "Update customer with delivery information",
                ],
            },
        )


class OllamaAIProvider:
    def generate_product_description(
        self,
        request: GenerateProductDescriptionRequest,
    ) -> ProductDescriptionData:
        product_name = _safe_get(request, "product_name", "")
        category = _safe_get(request, "category", "")
        features = _safe_get(request, "features", [])
        tone = _safe_get(request, "tone", "Professional")

        system_prompt = (
            "You are an expert e-commerce copywriter. "
            "Write clear, useful, conversion-focused product descriptions. "
            "Do not invent technical specs."
        )

        user_prompt = f"""
Product name: {product_name}
Category: {category}
Features: {", ".join(features)}
Tone: {tone}

Write a product description in 80-120 words.
"""

        content = ollama_provider.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return _build_pydantic_model(
            ProductDescriptionData,
            {
                "content": content,
                "description": content,
                "product_description": content,
                "product_name": product_name,
                "category": category,
                "provider": "ollama",
                "model_name": settings.OLLAMA_MODEL_NAME,
            },
        )

    def summarize_order_report(
        self,
        request: SummarizeOrderReportRequest,
    ) -> OrderReportSummaryData:
        report_title = _safe_get(request, "report_title", "")
        total_orders = _safe_get(request, "total_orders", 0)
        total_sales_amount = _safe_get(request, "total_sales_amount", 0)
        total_customers = _safe_get(request, "total_customers", 0)
        top_products = _safe_get(request, "top_products", [])

        system_prompt = (
            "You are a business analyst for an e-commerce company. "
            "Summarize order reports with clear insights and action points."
        )

        user_prompt = f"""
Report title: {report_title}
Total orders: {total_orders}
Total sales amount: {total_sales_amount}
Total customers: {total_customers}
Top products: {top_products}

Write a short business summary with 3 insights and 3 recommendations.
"""

        content = ollama_provider.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return _build_pydantic_model(
            OrderReportSummaryData,
            {
                "content": content,
                "summary": content,
                "report_title": report_title,
                "provider": "ollama",
                "model_name": settings.OLLAMA_MODEL_NAME,
            },
        )

    def generate_customer_support_reply(
        self,
        request: CustomerSupportReplyRequest,
    ) -> CustomerSupportReplyData:
        customer_message = _safe_get(request, "customer_message", "")
        order_status = _safe_get(request, "order_status", "")
        tone = _safe_get(request, "tone", "Professional")

        system_prompt = (
            "You are a helpful e-commerce customer support agent. "
            "Reply politely and clearly. Do not promise anything not confirmed."
        )

        user_prompt = f"""
Customer message:
{customer_message}

Current order status:
{order_status}

Tone:
{tone}

Write a customer support reply.
"""

        content = ollama_provider.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return _build_pydantic_model(
            CustomerSupportReplyData,
            {
                "content": content,
                "reply": content,
                "order_status": order_status,
                "tone": tone,
                "provider": "ollama",
                "model_name": settings.OLLAMA_MODEL_NAME,
            },
        )


class OpenAIProvider(OllamaAIProvider):
    """
    Temporary compatibility provider.
    Old code imports OpenAIProvider. For now, it delegates to Ollama.
    """
    pass


def get_ai_provider():
    provider = settings.AI_PROVIDER.lower()

    if provider == "ollama":
        return OllamaAIProvider()

    if provider == "openai":
        return OpenAIProvider()

    return MockAIProvider()
