from typing import List, Optional
from uuid import uuid4

from app.providers.embedding_provider import get_embedding_provider
from app.providers.rag_answer_provider import get_rag_answer_provider
from app.schemas.rag_schema import (
    RAGAskData,
    RAGDocumentIndexData,
    RAGDocumentIndexRequest,
    RAGSearchResult,
)
from app.vectorstores.file_vector_store import vector_store


class RAGService:
    def index_document(
        self,
        request: RAGDocumentIndexRequest,
    ) -> RAGDocumentIndexData:
        document_id = str(uuid4())

        chunks = self._chunk_text(
            text=request.content,
            max_words=80,
            overlap_words=20,
        )

        embedding_provider = get_embedding_provider()

        for chunk_text in chunks:
            chunk_id = str(uuid4())
            vector = embedding_provider.create_embedding(chunk_text)

            vector_store.add_chunk(
                chunk_id=chunk_id,
                document_id=document_id,
                title=request.title,
                content=chunk_text,
                vector=vector,
                source_type=request.source_type or "text",
            )

        return RAGDocumentIndexData(
            document_id=document_id,
            title=request.title,
            chunks_count=len(chunks),
        )

    def search(
        self,
        query: str,
        top_k: int,
        source_type: Optional[str] = None,
    ) -> List[RAGSearchResult]:
        embedding_provider = get_embedding_provider()
        query_vector = embedding_provider.create_embedding(query)

        return vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            source_type=source_type,
        )

    def ask(
        self,
        question: str,
        top_k: int,
        source_type: Optional[str] = None,
    ) -> RAGAskData:
        sources = self.search(
            query=question,
            top_k=top_k,
            source_type=source_type,
        )

        answer_provider = get_rag_answer_provider()

        answer = answer_provider.generate_answer(
            question=question,
            sources=sources,
        )

        return RAGAskData(
            answer=answer,
            sources=sources,
        )

    def _chunk_text(
        self,
        text: str,
        max_words: int,
        overlap_words: int,
    ) -> List[str]:
        words = text.split()

        if len(words) <= max_words:
            return [" ".join(words)]

        chunks: List[str] = []
        start = 0

        while start < len(words):
            end = start + max_words
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))

            if end >= len(words):
                break

            start = end - overlap_words

        return chunks


rag_service = RAGService()
