import math
from typing import Dict, List

from uuid import uuid4

from app.providers.embedding_provider import (
    EmbeddingVector,
    get_embedding_provider,
)
from app.schemas.rag_schema import (
    RAGAskData,
    RAGDocumentIndexData,
    RAGDocumentIndexRequest,
    RAGSearchResult,
)


class RAGService:
    def __init__(self):
        self.chunks: List[Dict] = []

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

            self.chunks.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": document_id,
                    "title": request.title,
                    "content": chunk_text,
                    "vector": embedding_provider.create_embedding(chunk_text),
                    "source_type": request.source_type,
                }
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
    ) -> List[RAGSearchResult]:
        embedding_provider = get_embedding_provider()
        query_vector = embedding_provider.create_embedding(query)

        results: List[RAGSearchResult] = []

        for chunk in self.chunks:
            score = self._cosine_similarity(
                query_vector,
                chunk["vector"],
            )

            if score <= 0:
                continue

            results.append(
                RAGSearchResult(
                    chunk_id=chunk["chunk_id"],
                    document_id=chunk["document_id"],
                    title=chunk["title"],
                    content=chunk["content"],
                    score=round(score, 4),
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return results[:top_k]

    def ask(
        self,
        question: str,
        top_k: int,
    ) -> RAGAskData:
        sources = self.search(
            query=question,
            top_k=top_k,
        )

        if not sources:
            return RAGAskData(
                answer="I could not find relevant information from the indexed documents.",
                sources=[],
            )

        best_source = sources[0]

        return RAGAskData(
            answer=best_source.content,
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

    def _cosine_similarity(
        self,
        vector_a: EmbeddingVector,
        vector_b: EmbeddingVector,
    ) -> float:
        if isinstance(vector_a, dict) and isinstance(vector_b, dict):
            return self._cosine_similarity_sparse(
                vector_a,
                vector_b,
            )

        if isinstance(vector_a, list) and isinstance(vector_b, list):
            return self._cosine_similarity_dense(
                vector_a,
                vector_b,
            )

        return 0.0

    def _cosine_similarity_sparse(
        self,
        vector_a: Dict[str, float],
        vector_b: Dict[str, float],
    ) -> float:
        if not vector_a or not vector_b:
            return 0.0

        common_tokens = set(vector_a.keys()) & set(vector_b.keys())

        dot_product = sum(
            vector_a[token] * vector_b[token]
            for token in common_tokens
        )

        magnitude_a = math.sqrt(
            sum(value * value for value in vector_a.values())
        )

        magnitude_b = math.sqrt(
            sum(value * value for value in vector_b.values())
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def _cosine_similarity_dense(
        self,
        vector_a: List[float],
        vector_b: List[float],
    ) -> float:
        if not vector_a or not vector_b:
            return 0.0

        if len(vector_a) != len(vector_b):
            return 0.0

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(value * value for value in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(value * value for value in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)


rag_service = RAGService()
