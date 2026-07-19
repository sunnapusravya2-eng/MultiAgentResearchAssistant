from __future__ import annotations

from sentence_transformers import SentenceTransformer

from app.core.config import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self, model_name: str = EMBEDDING_MODEL) -> None:
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            return []
        embedding = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return embedding.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        clean_texts = [text for text in texts if text.strip()]
        if not clean_texts:
            return []
        embeddings = self.model.encode(clean_texts, convert_to_numpy=True, normalize_embeddings=True)
        return [vector.tolist() for vector in embeddings]