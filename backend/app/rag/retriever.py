from __future__ import annotations

from typing import Any

from app.core.config import CHUNK_OVERLAP, MAX_CHUNK_SIZE
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import ChromaVectorStore
from app.utils.text_splitter import create_chunks_for_document


class RetrieverAgent:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()
        self.vector_store = ChromaVectorStore()

    def index_document(self, document_id: int, filename: str, text: str) -> None:
        chunks = create_chunks_for_document(text, max_chunk_size=MAX_CHUNK_SIZE, overlap=CHUNK_OVERLAP)
        if not chunks:
            return

        ids = [f"{document_id}_{index}" for index in range(len(chunks))]
        metadatas = [
            {"source": filename, "chunk_index": index, "document_id": document_id}
            for index in range(len(chunks))
        ]
        embeddings = self.embedding_service.embed_texts(chunks)
        self.vector_store.add_texts(ids=ids, texts=chunks, metadatas=metadatas, embeddings=embeddings)

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        query_embedding = self.embedding_service.embed_text(query)
        if not query_embedding:
            return []

        result = self.vector_store.query(query_embedding=query_embedding, top_k=top_k)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        ids = result.get("ids", [[]])[0]

        return [
            {
                "id": ids[idx],
                "text": documents[idx],
                "metadata": metadatas[idx] if idx < len(metadatas) else {},
                "distance": distances[idx] if idx < len(distances) else None,
            }
            for idx in range(len(documents))
        ]

    def build_context(self, query: str, top_k: int = 5) -> str:
        results = self.retrieve(query=query, top_k=top_k)
        context_segments = []
        for item in results:
            source = item["metadata"].get("source", "unknown")
            context_segments.append(f"[Source: {source}] {item['text']}")
        return "\n\n".join(context_segments)