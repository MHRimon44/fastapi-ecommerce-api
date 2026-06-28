import json
import math
from pathlib import Path
from typing import Dict, List, Optional

from app.providers.embedding_provider import EmbeddingVector
from app.schemas.rag_schema import RAGSearchResult


class FileVectorStore:
    def __init__(
        self,
        storage_path: Optional[str] = None,
    ):
        if storage_path is None:
            storage_path = "storage/vector_store.json"

        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def add_chunk(
        self,
        chunk_id: str,
        document_id: str,
        title: str,
        content: str,
        vector: EmbeddingVector,
        source_type: str,
    ) -> None:
        chunks = self._load_chunks()

        chunks.append(
            {
                "chunk_id": chunk_id,
                "document_id": document_id,
                "title": title,
                "content": content,
                "vector": vector,
                "source_type": source_type,
            }
        )

        self._save_chunks(chunks)

    def search(
        self,
        query_vector: EmbeddingVector,
        top_k: int,
        source_type: Optional[str] = None,
    ) -> List[RAGSearchResult]:
        chunks = self._load_chunks()
        results: List[RAGSearchResult] = []

        for chunk in chunks:
            if source_type and chunk.get("source_type") != source_type:
                continue

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

    def clear(self) -> None:
        self._save_chunks([])

    def count(self) -> int:
        return len(self._load_chunks())

    def _load_chunks(self) -> List[Dict]:
        if not self.storage_path.exists():
            return []

        try:
            content = self.storage_path.read_text()

            if not content.strip():
                return []

            data = json.loads(content)

            if not isinstance(data, list):
                return []

            return data

        except json.JSONDecodeError:
            return []

    def _save_chunks(
        self,
        chunks: List[Dict],
    ) -> None:
        self.storage_path.write_text(
            json.dumps(
                chunks,
                indent=2,
            )
        )

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


vector_store = FileVectorStore()
