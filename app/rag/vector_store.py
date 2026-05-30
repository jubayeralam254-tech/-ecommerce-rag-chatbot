from __future__ import annotations

from functools import lru_cache

from langchain_chroma import Chroma

from app.services.embedding_service import get_embedding_model
from app.utils.config import settings


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    return Chroma(
        collection_name=settings.chroma_collection,
        persist_directory=str(settings.chroma_dir),
        embedding_function=get_embedding_model(),
    )


def delete_source_chunks(source_id: str) -> None:
    # LangChain exposes the underlying Chroma collection here; good enough for a simple project.
    get_vector_store()._collection.delete(where={"source_id": source_id})
