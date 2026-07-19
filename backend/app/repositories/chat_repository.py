from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.models import ChatMessage


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add_message(self, conversation_id: str, role: str, content: str) -> ChatMessage:
        message = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_history(self, conversation_id: str) -> list[ChatMessage]:
        return (
            self.db.query(ChatMessage)
            .filter(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )