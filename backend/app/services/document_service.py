from __future__ import annotations

import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import UPLOAD_DIR
from app.core.database import SessionLocal
from app.core.logging import logger
from app.repositories.document_repository import DocumentRepository
from app.rag.retriever import RetrieverAgent
from app.utils.file_utils import SUPPORTED_EXTENSIONS, extract_text


class DocumentService:
    def __init__(self, upload_dir: str | Path | None = None) -> None:
        self.upload_dir = Path(upload_dir or UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.retriever = RetrieverAgent()

    def process_upload(self, uploaded_file: UploadFile) -> dict[str, Any]:
        if uploaded_file.filename is None or not uploaded_file.filename.strip():
            raise ValueError("The uploaded file is missing a filename.")

        file_bytes = uploaded_file.file.read()
        return self.process_bytes(filename=uploaded_file.filename, file_bytes=file_bytes)

    def process_bytes(self, filename: str, file_bytes: bytes) -> dict[str, Any]:
        safe_filename = Path(filename).name.strip()
        if not safe_filename:
            raise ValueError("The uploaded file is missing a filename.")

        extension = Path(safe_filename).suffix.lower()
        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
            )

        temp_path: Path | None = None
        saved_path: Path | None = None
        try:
            with NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
                temp_file.write(file_bytes)
                temp_path = Path(temp_file.name)

            extracted_text = extract_text(temp_path)
            saved_path = self._save_to_storage(safe_filename, temp_path)
            document_id = self._save_document_record(safe_filename, str(saved_path), extracted_text)
            self.retriever.index_document(document_id=document_id, filename=safe_filename, text=extracted_text)

            logger.info("Saved uploaded document %s to %s", safe_filename, saved_path)
            return {
                "filename": safe_filename,
                "file_path": str(saved_path),
                "extracted_text": extracted_text,
                "document_id": document_id,
            }
        except FileNotFoundError as exc:
            logger.warning("File not found during upload: %s", safe_filename)
            raise RuntimeError(f"Uploaded file not found: {safe_filename}") from exc
        except ValueError as exc:
            logger.warning("Validation failed for file %s: %s", safe_filename, exc)
            raise
        except Exception as exc:
            logger.exception("Failed to process uploaded file %s", safe_filename)
            raise RuntimeError(f"Failed to process upload: {safe_filename}") from exc
        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)

    def _save_to_storage(self, filename: str, temp_path: Path) -> Path:
        destination = self.upload_dir / filename
        destination = self._make_unique_path(destination)
        temp_path.replace(destination)
        return destination

    def _make_unique_path(self, path: Path) -> Path:
        if not path.exists():
            return path
        counter = 1
        stem = path.stem
        suffix = path.suffix
        while True:
            candidate = path.with_name(f"{stem}_{counter}{suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def _save_document_record(self, filename: str, file_path: str, extracted_text: str) -> int:
        session: Session = SessionLocal()
        try:
            repository = DocumentRepository(session)
            document = repository.create(filename=filename, file_path=file_path, extracted_text=extracted_text)
            return document.id
        finally:
            session.close()