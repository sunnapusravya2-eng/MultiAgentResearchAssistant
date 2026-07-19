from __future__ import annotations

from app.rag.retriever import RetrieverAgent as RetrieverService


class RetrieverAgent:
    def __init__(self) -> None:
        self.service = RetrieverService()

    def retrieve(self, question: str) -> list[dict[str, str]]:
        results = self.service.retrieve(question, top_k=5)
        return [
            {
                "source": item["metadata"].get("source", "unknown"),
                "text": item["text"],
                "distance": item["distance"],
            }
            for item in results
        ]