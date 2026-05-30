from __future__ import annotations

import asyncio

from fastapi import APIRouter, HTTPException, status

from app.schemas import AskRequest, AskResponse
from app.rag.retriever import retrieve_relevant_chunks
from app.services.gemini_service import generate_answer

router = APIRouter(tags=["chat"])


@router.post("/ask", response_model=AskResponse)
async def ask_question(payload: AskRequest):
    try:
        retrieved_context, sources = await asyncio.to_thread(
            retrieve_relevant_chunks,
            payload.question,
            payload.top_k,
        )

        answer = await asyncio.to_thread(generate_answer, payload.question, retrieved_context)

        if not answer:
            answer = "I could not generate an answer from the uploaded PDFs."

        return AskResponse(answer=answer, retrieved_context=retrieved_context, sources=sources)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to answer question") from exc
