from typing import List

from app.schemas.erp_policy_schema import (
    ERPPolicyAskRequest,
    ERPPolicyIndexData,
    ERPPolicyIndexRequest,
    ERPPolicySearchRequest,
)
from app.schemas.rag_schema import (
    RAGAskData,
    RAGDocumentIndexRequest,
    RAGSearchResult,
)
from app.services.rag_service import rag_service


ERP_POLICY_SOURCE_TYPE = "erp_policy"


class ERPPolicyService:
    def index_policy(
        self,
        request: ERPPolicyIndexRequest,
    ) -> ERPPolicyIndexData:
        content = self._build_policy_content(request)

        indexed_data = rag_service.index_document(
            RAGDocumentIndexRequest(
                title=request.policy_title,
                content=content,
                source_type=ERP_POLICY_SOURCE_TYPE,
            )
        )

        return ERPPolicyIndexData(
            document_id=indexed_data.document_id,
            policy_title=request.policy_title,
            chunks_count=indexed_data.chunks_count,
        )

    def search_policies(
        self,
        request: ERPPolicySearchRequest,
    ) -> List[RAGSearchResult]:
        return rag_service.search(
            query=request.query,
            top_k=request.top_k,
            source_type=ERP_POLICY_SOURCE_TYPE,
        )

    def ask_policy_question(
        self,
        request: ERPPolicyAskRequest,
    ) -> RAGAskData:
        return rag_service.ask(
            question=request.question,
            top_k=request.top_k,
            source_type=ERP_POLICY_SOURCE_TYPE,
        )

    def _build_policy_content(
        self,
        request: ERPPolicyIndexRequest,
    ) -> str:
        lines = [
            f"Policy Title: {request.policy_title}",
            f"Policy Content: {request.policy_content}",
        ]

        if request.module_name:
            lines.append(f"ERP Module: {request.module_name}")

        if request.department:
            lines.append(f"Department: {request.department}")

        if request.rules:
            lines.append("Rules: " + " | ".join(request.rules))

        if request.tags:
            lines.append("Tags: " + ", ".join(request.tags))

        return "\n".join(lines)


erp_policy_service = ERPPolicyService()
