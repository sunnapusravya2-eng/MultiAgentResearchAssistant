from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.database import Base, engine, get_db
from app.core.logging import logger
from app.repositories.document_repository import DocumentRepository
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.report_service import ReportService

router = APIRouter()


@router.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    UploadDir = Path(UPLOAD_DIR)
    UploadDir.mkdir(parents=True, exist_ok=True)


@router.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/documents/upload", tags=["documents"])
async def upload_documents(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    service = DocumentService()
    documents = []
    for uploaded_file in files:
        try:
            result = service.process_upload(uploaded_file)
            documents.append(result)
        except ValueError as exc:
            logger.warning("Validation error on upload: %s", exc)
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except RuntimeError as exc:
            logger.exception("Processing failed for file %s", uploaded_file.filename)
            raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"documents": documents}


@router.post("/chat", tags=["chat"])
async def chat(
    question: dict[str, str],
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    user_question = question.get("question", "").strip()
    conversation_id = question.get("conversation_id", "default")
    if not user_question:
        raise HTTPException(status_code=400, detail="Question is required.")

    service = ChatService()
    try:
        response = service.create_response(user_question, conversation_id)
        return response
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Chat request failed")
        raise HTTPException(status_code=500, detail="Chat service failed.") from exc


@router.post("/reports/generate", tags=["reports"])
async def generate_report(payload: dict[str, str]) -> dict[str, Any]:
    title = payload.get("title", "").strip()
    question = payload.get("question", "").strip()
    conversation_id = payload.get("conversation_id", "default")

    if not title or not question:
        raise HTTPException(status_code=400, detail="Report title and question are required.")

    service = ReportService()
    try:
        report_info = service.generate_report(title=title, question=question, conversation_id=conversation_id)
        return report_info
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Report generation failed")
        raise HTTPException(status_code=500, detail="Failed to generate report.") from exc