from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings

from app.core.config import CHROMA_DIR


class ChromaVectorStore:
    def __init__(self, persist_directory: str | Path | None = None, collection_name: str = "research_assistant"):
        self.persist_directory = Path(persist_directory or CHROMA_DIR)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_texts(self, ids: list[str], texts: list[str], metadatas: list[dict[str, Any]], embeddings: list[list[float]]) -> None:
        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, query_embedding: list[float], top_k: int = 5) -> dict[str, list[Any]]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
           include=["documents", "metadatas", "distances"],
        )
        return result