from __future__ import annotations

from fastapi import FastAPI

from app.routes.chat import router as chat_router
from app.routes.upload import router as upload_router
from app.schemas import HealthResponse
from app.utils.config import settings

app = FastAPI(
    title="AI PDF Chat API",
    description="Upload PDFs, index them in ChromaDB, and ask questions with Gemini.",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")


app.include_router(upload_router)
app.include_router(chat_router)
