from __future__ import annotations

import csv
from pathlib import Path
from typing import Final

from docx import Document as DocxDocument
from pypdf import PdfReader

from app.core.logging import logger

SUPPORTED_EXTENSIONS: Final[dict[str, str]] = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".txt": "txt",
    ".csv": "csv",
}


def extract_text(file_path: str | Path) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {suffix}. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    try:
        if suffix == ".pdf":
            return _extract_text_from_pdf(path)
        if suffix == ".docx":
            return _extract_text_from_docx(path)
        if suffix == ".txt":
            return _extract_text_from_txt(path)
        if suffix == ".csv":
            return _extract_text_from_csv(path)

        raise ValueError(f"Unsupported file type: {suffix}")
    except Exception as exc:
        logger.exception("Failed to extract text from %s", path.name)
        raise RuntimeError(f"Failed to parse file: {path.name}") from exc


def _extract_text_from_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    content_parts: list[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            content_parts.append(text.strip())
    return "\n\n".join(content_parts).strip()


def _extract_text_from_docx(file_path: Path) -> str:
    document = DocxDocument(str(file_path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text and paragraph.text.strip()]
    return "\n\n".join(paragraphs).strip()


def _extract_text_from_txt(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        return handle.read()


def _extract_text_from_csv(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8-sig", newline="", errors="ignore") as handle:
        rows = list(csv.reader(handle))
    return "\n".join(" | ".join(row) for row in rows if row)