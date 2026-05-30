from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    top_k: int = Field(default=4, ge=1, le=10, description="Number of chunks to retrieve")


class AskResponse(BaseModel):
    answer: str
    retrieved_context: list[str]
    sources: list[dict]


class UploadResponse(BaseModel):
    message: str
    filename: str
    stored_path: str
    chunks_indexed: int
    collection_name: str


class HealthResponse(BaseModel):
    status: str