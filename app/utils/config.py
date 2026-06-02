from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
    embedding_model_name: str = os.getenv(
    "EMBEDDING_MODEL", "models/embedding-001"  # ← এটা change কর
)
    chroma_dir: Path = PROJECT_ROOT / os.getenv("CHROMA_DIR", "app/chroma_db")
    upload_dir: Path = PROJECT_ROOT / os.getenv("UPLOAD_DIR", "app/uploads")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "pdf_knowledge_base")
    chunk_size: int = _env_int("CHUNK_SIZE", 1000)
    chunk_overlap: int = _env_int("CHUNK_OVERLAP", 200)
    top_k: int = _env_int("TOP_K", 4)

    def ensure_directories(self) -> None:
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()