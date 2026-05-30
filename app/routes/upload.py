from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas import UploadResponse
from app.services.pdf_service import load_pdf_documents, save_uploaded_pdf, split_documents
from app.rag.vector_store import delete_source_chunks, get_vector_store
from app.utils.config import settings

router = APIRouter(tags=["upload"])


@router.post("/upload-pdf", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File(...)):
    try:
        stored_path, source_id = await save_uploaded_pdf(file)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save file") from exc

    try:
        documents = load_pdf_documents(stored_path)
        chunks = split_documents(documents)
        if not chunks:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No text found in PDF")

        vector_store = get_vector_store()
        delete_source_chunks(source_id)

        ids = []
        for index, chunk in enumerate(chunks):
            chunk.metadata.update(
                {
                    "source_id": source_id,
                    "source": file.filename,
                    "chunk_index": index,
                }
            )
            ids.append(f"{source_id}_{index}")

        vector_store.add_documents(chunks, ids=ids)

        return UploadResponse(
            message="PDF uploaded and indexed successfully",
            filename=file.filename or stored_path.name,
            stored_path=str(stored_path),
            chunks_indexed=len(chunks),
            collection_name=settings.chroma_collection,
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process PDF") from exc
