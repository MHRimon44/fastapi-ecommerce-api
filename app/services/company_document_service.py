from typing import List

from app.schemas.company_document_schema import (
    CompanyDocumentAskRequest,
    CompanyDocumentIndexData,
    CompanyDocumentIndexRequest,
    CompanyDocumentSearchRequest,
)
from app.schemas.rag_schema import (
    RAGAskData,
    RAGDocumentIndexRequest,
    RAGSearchResult,
)
from app.services.rag_service import rag_service


COMPANY_DOCUMENT_SOURCE_TYPE = "company_document"


class CompanyDocumentService:
    def index_document(
        self,
        request: CompanyDocumentIndexRequest,
    ) -> CompanyDocumentIndexData:
        content = self._build_company_document_content(request)

        indexed_data = rag_service.index_document(
            RAGDocumentIndexRequest(
                title=request.document_title,
                content=content,
                source_type=COMPANY_DOCUMENT_SOURCE_TYPE,
            )
        )

        return CompanyDocumentIndexData(
            document_id=indexed_data.document_id,
            document_title=request.document_title,
            chunks_count=indexed_data.chunks_count,
        )

    def search_documents(
        self,
        request: CompanyDocumentSearchRequest,
    ) -> List[RAGSearchResult]:
        return rag_service.search(
            query=request.query,
            top_k=request.top_k,
            source_type=COMPANY_DOCUMENT_SOURCE_TYPE,
        )

    def ask_document_question(
        self,
        request: CompanyDocumentAskRequest,
    ) -> RAGAskData:
        return rag_service.ask(
            question=request.question,
            top_k=request.top_k,
            source_type=COMPANY_DOCUMENT_SOURCE_TYPE,
        )

    def _build_company_document_content(
        self,
        request: CompanyDocumentIndexRequest,
    ) -> str:
        lines = [
            f"Document Title: {request.document_title}",
            f"Content: {request.content}",
        ]

        if request.department:
            lines.append(f"Department: {request.department}")

        if request.document_type:
            lines.append(f"Document Type: {request.document_type}")

        if request.tags:
            lines.append("Tags: " + ", ".join(request.tags))

        return "\n".join(lines)


company_document_service = CompanyDocumentService()
