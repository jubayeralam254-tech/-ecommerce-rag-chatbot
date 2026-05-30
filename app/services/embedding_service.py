from __future__ import annotations

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.utils.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    # Local embeddings keep the project simple and avoid another API key.
    return HuggingFaceEmbeddings(model_name=settings.embedding_model_name)
