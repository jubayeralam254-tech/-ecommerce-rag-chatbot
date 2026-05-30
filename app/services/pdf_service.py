from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.utils.config import settings


async def save_uploaded_pdf(upload_file: UploadFile) -> tuple[Path, str]:
    if not upload_file.filename or not upload_file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")

    safe_name = Path(upload_file.filename).name
    stored_name = f"{uuid4().hex}_{safe_name}"
    stored_path = settings.upload_dir / stored_name

    content_hash = hashlib.sha256()
    with stored_path.open("wb") as buffer:
        while True:
            chunk = await upload_file.read(1024 * 1024)
            if not chunk:
                break
            content_hash.update(chunk)
            buffer.write(chunk)

    await upload_file.close()
    return stored_path, content_hash.hexdigest()


def load_pdf_documents(pdf_path: Path):
    loader = PyPDFLoader(str(pdf_path))
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)
