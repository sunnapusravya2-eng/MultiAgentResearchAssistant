from __future__ import annotations

from typing import Any
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.logging import logger
from app.prompts.prompts import build_chat_prompt
from app.repositories.chat_repository import ChatRepository
from app.rag.retriever import RetrieverAgent
from app.services.llm_service import create_llm


class ChatService:
    def __init__(self) -> None:
        self.retriever = RetrieverAgent()
        self.llm = create_llm()

    def create_response(self, question: str, conversation_id: str) -> dict[str, Any]:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        context = self.retriever.build_context(question, top_k=5)
        history = self._load_history(conversation_id)
        prompt = build_chat_prompt(question=question, context=context, history=history)

        logger.info("Sending query to Gemini for conversation %s", conversation_id)
        answer = self.llm.invoke(prompt).content

        self._save_message(conversation_id, "user", question)
        self._save_message(conversation_id, "assistant", answer)

        citations = self._extract_citations(answer)
        return {"answer": answer, "citations": citations, "conversation_id": conversation_id}

    def _load_history(self, conversation_id: str) -> list[dict[str, str]]:
        session: Session = SessionLocal()
        try:
            repository = ChatRepository(session)
            messages = repository.get_history(conversation_id)
            return [{"role": message.role, "content": message.content} for message in messages]
        finally:
            session.close()

    def _save_message(self, conversation_id: str, role: str, content: str) -> None:
        session: Session = SessionLocal()
        try:
            repository = ChatRepository(session)
            repository.add_message(conversation_id=conversation_id, role=role, content=content)
        finally:
            session.close()

    @staticmethod
    def _extract_citations(answer: str) -> list[str]:
        citations: list[str] = []
        for line in answer.splitlines():
            if line.strip().startswith("[Source:"):
                citations.append(line.strip())
        return citations