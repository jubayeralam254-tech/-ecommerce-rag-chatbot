from __future__ import annotations

from google import genai

from app.utils.config import settings


def generate_answer(question: str, retrieved_context: list[str]) -> str:
    if not settings.google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing")

    client = genai.Client(api_key=settings.google_api_key)
    context_text = "\n\n".join(f"- {chunk}" for chunk in retrieved_context)

    prompt = f"""
You are a helpful PDF question-answering assistant.
Use only the context below.
If the answer is not in the context, say you cannot find it in the uploaded PDF.

Context:
{context_text}

Question: {question}

Answer clearly and briefly.
""".strip()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )
    return (response.text or "").strip()