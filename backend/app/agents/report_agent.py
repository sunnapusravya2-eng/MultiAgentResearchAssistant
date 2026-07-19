from __future__ import annotations

from app.services.llm_service import create_llm


class ReportAgent:
    def __init__(self) -> None:
        self.llm = create_llm()

    def build_report(self, question: str, summary: str, citations: str) -> str:
        prompt = (
            "Use the following summary and citations to build a polished research report.\n\n"
            f"Question:\n{question}\n\n"
            f"Summary:\n{summary}\n\n"
            f"Citations:\n{citations}"
        )
        return self.llm(prompt)