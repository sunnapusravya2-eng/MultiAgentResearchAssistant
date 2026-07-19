from __future__ import annotations

from app.prompts.prompts import build_chat_prompt
from app.services.llm_service import create_llm


class ResearchAgent:
    def __init__(self) -> None:
        self.llm = create_llm()

    def research(self, question: str, retrieved_results: list[dict[str, str]]) -> str:
        context = "\n\n".join(
            f"[Source: {item['source']}]\n{item['text']}" for item in retrieved_results
        )
        prompt = build_chat_prompt(question=question, context=context, history=[])
        return self.llm(prompt)