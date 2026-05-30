from __future__ import annotations

from app.rag.vector_store import get_vector_store


def retrieve_relevant_chunks(question: str, top_k: int):
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(question, k=top_k)

    chunks: list[str] = []
    sources: list[dict] = []

    for doc, score in results:
        chunks.append(doc.page_content)
        sources.append(
            {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "chunk_index": doc.metadata.get("chunk_index"),
                "score": score,
            }
        )

    return chunks, sources
