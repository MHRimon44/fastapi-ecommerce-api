from typing import List

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

        audience_text = "general customers"
        if request.target_audience:
            audience_text = request.target_audience

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
            provider=settings.AI_PROVIDER,
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
            insights.append(
                "Top products: " + ", ".join(request.top_products)
            )

        if request.note:
            insights.append(
                "Business note: " + request.note
            )

        return OrderReportSummaryData(
            summary=summary,
            insights=insights,
            provider=settings.AI_PROVIDER,
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
            provider=settings.AI_PROVIDER,
            model_name=settings.AI_MODEL_NAME,
        )
