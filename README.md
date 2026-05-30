# AI PDF Chat API

Simple backend project for chatting with uploaded PDF files using FastAPI, LangChain, ChromaDB, and Google Gemini.

## What it does

- Upload PDF files through an API endpoint
- Extract text from PDFs
- Split text into overlapping chunks
- Generate embeddings and store them in persistent ChromaDB
- Ask questions against the uploaded PDFs
- Return clean JSON responses

## Project structure

```text
app/
├── main.py
├── routes/
│   ├── upload.py
│   └── chat.py
├── services/
│   ├── pdf_service.py
│   ├── embedding_service.py
│   └── gemini_service.py
├── rag/
│   ├── retriever.py
│   └── vector_store.py
├── utils/
│   └── config.py
├── schemas.py
├── uploads/
└── chroma_db/
```

## Setup

1. Create and activate a virtual environment.

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file from `.env.example` and set your Google API key.

4. Run the API:

```powershell
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /upload-pdf`
- `POST /ask`

## Example requests

Upload a PDF:

```powershell
curl -F "file=@sample.pdf" http://127.0.0.1:8000/upload-pdf
```

Ask a question:

```powershell
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"What is this PDF about?"}'
```

## Notes

- PDFs are stored locally in `app/uploads/`.
- ChromaDB persists to `app/chroma_db/`.
- Embeddings use a local SentenceTransformer model, so no embedding API key is needed.
- Gemini is used only for the final answer generation.