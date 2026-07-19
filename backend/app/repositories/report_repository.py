from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.models import Report


class ReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, title: str, prompt: str, content: str, pdf_path: str, docx_path: str) -> Report:
        report = Report(
            title=title,
            prompt=prompt,
            content=content,
            pdf_path=pdf_path,
            docx_path=docx_path,
        )
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_all(self) -> list[Report]:
        return self.db.query(Report).order_by(Report.created_at.desc()).all()