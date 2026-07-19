from typing import List

from sqlalchemy import distinct

from app.core.database import SessionLocal
from app.models.models import ChatMessage


def get_conversation_messages(conversation_id: str) -> List[ChatMessage]:
    with SessionLocal() as db:
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )


def list_conversations(limit: int = 50) -> List[str]:
    with SessionLocal() as db:
        conversation_ids = (
            db.query(distinct(ChatMessage.conversation_id))
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )
        return [row[0] for row in conversation_ids]


def add_message(conversation_id: str, role: str, content: str) -> ChatMessage:
    with SessionLocal() as db:
        message = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
