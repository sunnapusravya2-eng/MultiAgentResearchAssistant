from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.models import Document


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, filename: str, file_path: str, extracted_text: str, source: str | None = None) -> Document:
        document = Document(
            filename=filename,
            file_path=file_path,
            extracted_text=extracted_text,
            source=source or filename,
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def list_all(self) -> list[Document]:
        return self.db.query(Document).order_by(Document.uploaded_at.desc()).all()

    def get_by_id(self, document_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == document_id).first()