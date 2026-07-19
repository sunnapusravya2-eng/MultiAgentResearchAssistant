from __future__ import annotations

from typing import Any

from app.services.llm_service import create_llm


class CitationAgent:
    def __init__(self) -> None:
        self.llm = create_llm()

    def verify(self, summary: str, retrieved_docs: list[dict[str, Any]]) -> str:
        sources = "\n\n".join(
            f"[Source: {item['source']}]\n{item['text']}" for item in retrieved_docs
        )
        prompt = (
            "Verify the citations in the summary and ensure each claim is traced "
            "to a source. Use the following documents:\n\n"
            f"{sources}\n\nSummary:\n{summary}"
        )
        return self.llm(prompt)