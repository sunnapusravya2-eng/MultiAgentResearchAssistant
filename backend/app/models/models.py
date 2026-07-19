from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=False)
    extracted_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    source = Column(String(255), nullable=True)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(128), nullable=False, index=True)
    role = Column(String(32), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    prompt = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    pdf_path = Column(String(1024), nullable=False)
    docx_path = Column(String(1024), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)