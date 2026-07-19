from __future__ import annotations

from app.services.llm_service import create_llm


class SummarizerAgent:
    def __init__(self) -> None:
        self.llm = create_llm()

    def summarize(self, content: str) -> str:
        prompt = (
            "Summarize the following research findings in a professional style.\n\n"
            f"{content}"
        )
        return self.llm(prompt)