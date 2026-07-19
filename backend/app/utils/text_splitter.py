from __future__ import annotations

from typing import Iterable


def chunk_text(text: str, max_chunk_size: int, overlap: int) -> list[str]:
    cleaned = " ".join(text.split())
    if not cleaned:
        return []

    words = cleaned.split(" ")
    if len(words) <= max_chunk_size:
        return [cleaned]

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + max_chunk_size, len(words))
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break
        start = max(0, end - overlap)

    return chunks


def create_chunks_for_document(text: str, max_chunk_size: int, overlap: int) -> list[str]:
    return chunk_text(text, max_chunk_size=max_chunk_size, overlap=overlap)