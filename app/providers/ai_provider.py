import json
from typing import List

from fastapi import HTTPException, status
from openai import APIError, OpenAI

from app.core.config import settings
from app.schemas.ai_schema import (
    CustomerSupportReplyData,
    CustomerSupportReplyRequest,
    GenerateProductDescriptionRequest,
    OrderReportSummaryData,
    ProductDescriptionData,
    SummarizeOrderReportRequest,
)


class MockAIProvider:
    def generate_product_description(
        self,
        request: GenerateProductDescriptionRequest,
    ) -> ProductDescriptionData:
        features_text = ", ".join(request.features)
        audience_text = request.target_audience or "general customers"

        description = (
            f"{request.product_name} is a {request.tone} product designed for "
            f"{audience_text}. It includes {features_text}, making it suitable "
            f"for modern e-commerce customers."
        )

        bullet_points: List[str] = []

        for feature in request.features:
            bullet_points.append(f"Includes {feature}")

        return ProductDescriptionData(
            description=description,
            bullet_points=bullet_points,
            provider="mock",
            model_name=settings.AI_MODEL_NAME,
        )

    def summarize_order_report(
        self,
        request: SummarizeOrderReportRequest,
    ) -> OrderReportSummaryData:
        average_order_value = 0

        if request.total_orders > 0:
            average_order_value = request.total_sales_amount / request.total_orders

        summary = (
            f"{request.report_title}: Total {request.total_orders} orders were placed "
            f"by {request.total_customers} customers, generating sales of "
            f"{request.total_sales_amount:.2f}. The average order value is "
            f"{average_order_value:.2f}."
        )

        insights = [
            f"Total orders: {request.total_orders}",
            f"Total sales amount: {request.total_sales_amount:.2f}",
            f"Average order value: {average_order_value:.2f}",
        ]

        if request.top_products:
            insights.append("Top products: " + ", ".join(request.top_products))

        if request.note:
            insights.append("Business note: " + request.note)

        return OrderReportSummaryData(
            summary=summary,
            insights=insights,
            provider="mock",
            model_name=settings.AI_MODEL_NAME,
        )

    def generate_customer_support_reply(
        self,
        request: CustomerSupportReplyRequest,
    ) -> CustomerSupportReplyData:
        customer_name = request.customer_name or "Customer"

        order_text = ""
        if request.order_no:
            order_text = f" regarding order {request.order_no}"

        reply = (
            f"Dear {customer_name}, thank you for contacting us{order_text}. "
            f"We have received your message: \"{request.customer_message}\". "
            f"Our support team will review this and assist you as soon as possible."
        )

        suggested_actions = [
            "Check customer order history",
            "Verify payment and delivery status",
            "Reply to customer with clear next steps",
        ]

        return CustomerSupportReplyData(
            reply=reply,
            suggested_actions=suggested_actions,
            provider="mock",
            model_name=settings.AI_MODEL_NAME,
        )


class OpenAIProvider:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="OPENAI_API_KEY is not configured",
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=30.0,
        )

    def _request_json_from_ai(
        self,
        prompt: str,
    ) -> dict:
        try:
            response = self.client.responses.create(
                model=settings.AI_MODEL_NAME,
                instructions=(
                    "You are an ecommerce AI assistant. "
                    "Return only valid JSON. Do not include markdown."
                ),
                input=prompt,
            )

            return json.loads(response.output_text)

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider returned invalid JSON",
            )

        except APIError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI provider request failed",
            )

    def generate_product_description(
        self,
        request: GenerateProductDescriptionRequest,
    ) -> ProductDescriptionData:
        prompt = f"""
Generate an ecommerce product description.

Product name: {request.product_name}
Features: {", ".join(request.features)}
Target audience: {request.target_audience or "general ecommerce customers"}
Tone: {request.tone}

Return JSON only:
{{
  "description": "clear ecommerce product description",
  "bullet_points": [
    "bullet point 1",
    "bullet point 2",
    "bullet point 3"
  ]
}}
"""

        data = self._request_json_from_ai(prompt)

        return ProductDescriptionData(
            description=data["description"],
            bullet_points=data["bullet_points"],
            provider="openai",
            model_name=settings.AI_MODEL_NAME,
        )

    def summarize_order_report(
        self,
        request: SummarizeOrderReportRequest,
    ) -> OrderReportSummaryData:
        prompt = f"""
Summarize this ecommerce order report.

Report title: {request.report_title}
Total orders: {request.total_orders}
Total sales amount: {request.total_sales_amount}
Total customers: {request.total_customers}
Top products: {", ".join(request.top_products)}
Note: {request.note or ""}

Return JSON only:
{{
  "summary": "business summary",
  "insights": [
    "insight 1",
    "insight 2",
    "insight 3"
  ]
}}
"""

        data = self._request_json_from_ai(prompt)

        return OrderReportSummaryData(
            summary=data["summary"],
            insights=data["insights"],
            provider="openai",
            model_name=settings.AI_MODEL_NAME,
        )

    def generate_customer_support_reply(
        self,
        request: CustomerSupportReplyRequest,
    ) -> CustomerSupportReplyData:
        prompt = f"""
Generate a customer support reply.

Customer name: {request.customer_name or "Customer"}
Order no: {request.order_no or ""}
Customer message: {request.customer_message}
Tone: {request.tone}

Return JSON only:
{{
  "reply": "support reply message",
  "suggested_actions": [
    "action 1",
    "action 2",
    "action 3"
  ]
}}
"""

        data = self._request_json_from_ai(prompt)

        return CustomerSupportReplyData(
            reply=data["reply"],
            suggested_actions=data["suggested_actions"],
            provider="openai",
            model_name=settings.AI_MODEL_NAME,
        )
