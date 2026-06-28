from typing import List

from app.schemas.rag_schema import (
    RAGAskData,
    RAGDocumentIndexRequest,
    RAGSearchResult,
)
from app.schemas.support_knowledge_schema import (
    SupportKnowledgeAskRequest,
    SupportKnowledgeIndexData,
    SupportKnowledgeIndexRequest,
    SupportKnowledgeSearchRequest,
)
from app.services.rag_service import rag_service


SUPPORT_KNOWLEDGE_SOURCE_TYPE = "customer_support_knowledge"


class SupportKnowledgeService:
    def index_support_knowledge(
        self,
        request: SupportKnowledgeIndexRequest,
    ) -> SupportKnowledgeIndexData:
        content = self._build_support_knowledge_content(request)

        indexed_data = rag_service.index_document(
            RAGDocumentIndexRequest(
                title=request.title,
                content=content,
                source_type=SUPPORT_KNOWLEDGE_SOURCE_TYPE,
            )
        )

        return SupportKnowledgeIndexData(
            document_id=indexed_data.document_id,
            title=request.title,
            chunks_count=indexed_data.chunks_count,
        )

    def search_support_knowledge(
        self,
        request: SupportKnowledgeSearchRequest,
    ) -> List[RAGSearchResult]:
        return rag_service.search(
            query=request.query,
            top_k=request.top_k,
            source_type=SUPPORT_KNOWLEDGE_SOURCE_TYPE,
        )

    def ask_support_question(
        self,
        request: SupportKnowledgeAskRequest,
    ) -> RAGAskData:
        return rag_service.ask(
            question=request.question,
            top_k=request.top_k,
            source_type=SUPPORT_KNOWLEDGE_SOURCE_TYPE,
        )

    def _build_support_knowledge_content(
        self,
        request: SupportKnowledgeIndexRequest,
    ) -> str:
        lines = [
            f"Title: {request.title}",
            f"Content: {request.content}",
        ]

        if request.issue_type:
            lines.append(f"Issue Type: {request.issue_type}")

        if request.resolution_steps:
            lines.append(
                "Resolution Steps: " + " | ".join(request.resolution_steps)
            )

        if request.tags:
            lines.append("Tags: " + ", ".join(request.tags))

        return "\n".join(lines)


support_knowledge_service = SupportKnowledgeService()
