from typing import List

from app.schemas.product_knowledge_schema import (
    ProductKnowledgeAskRequest,
    ProductKnowledgeIndexData,
    ProductKnowledgeIndexRequest,
    ProductKnowledgeSearchRequest,
)
from app.schemas.rag_schema import (
    RAGAskData,
    RAGDocumentIndexRequest,
    RAGSearchResult,
)
from app.services.rag_service import rag_service


PRODUCT_KNOWLEDGE_SOURCE_TYPE = "product_knowledge"


class ProductKnowledgeService:
    def index_product(
        self,
        request: ProductKnowledgeIndexRequest,
    ) -> ProductKnowledgeIndexData:
        content = self._build_product_knowledge_content(request)

        indexed_data = rag_service.index_document(
            RAGDocumentIndexRequest(
                title=request.product_name,
                content=content,
                source_type=PRODUCT_KNOWLEDGE_SOURCE_TYPE,
            )
        )

        return ProductKnowledgeIndexData(
            document_id=indexed_data.document_id,
            product_name=request.product_name,
            chunks_count=indexed_data.chunks_count,
        )

    def search_products(
        self,
        request: ProductKnowledgeSearchRequest,
    ) -> List[RAGSearchResult]:
        return rag_service.search(
            query=request.query,
            top_k=request.top_k,
            source_type=PRODUCT_KNOWLEDGE_SOURCE_TYPE,
        )

    def ask_product_question(
        self,
        request: ProductKnowledgeAskRequest,
    ) -> RAGAskData:
        return rag_service.ask(
            question=request.question,
            top_k=request.top_k,
            source_type=PRODUCT_KNOWLEDGE_SOURCE_TYPE,
        )

    def _build_product_knowledge_content(
        self,
        request: ProductKnowledgeIndexRequest,
    ) -> str:
        lines = [
            f"Product Name: {request.product_name}",
            f"Description: {request.description}",
        ]

        if request.sku:
            lines.append(f"SKU: {request.sku}")

        if request.category:
            lines.append(f"Category: {request.category}")

        if request.features:
            lines.append("Features: " + ", ".join(request.features))

        if request.price is not None:
            lines.append(f"Price: {request.price}")

        if request.stock_qty is not None:
            lines.append(f"Stock Quantity: {request.stock_qty}")

        if request.use_case:
            lines.append(f"Use Case: {request.use_case}")

        return "\n".join(lines)


product_knowledge_service = ProductKnowledgeService()
