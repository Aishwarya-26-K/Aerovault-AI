"""
Central configuration for the Aviation RAG system.

All settings are loaded from environment variables (or a .env file).
This keeps secrets out of code and makes deployment predictable.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root = parent of the `app/` package
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings with sensible defaults for local development."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------------
    # LLM Configuration
    # -------------------------
    llm_provider: str = Field(
        default="gemini",
        validation_alias="LLM_PROVIDER",
    )

    google_api_key: str | None = Field(
        default=None,
        validation_alias="GOOGLE_API_KEY",
    )

    openai_api_key: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )


    # -------------------------
    # Embeddings
    # -------------------------
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        validation_alias="EMBEDDING_MODEL",
    )


    # -------------------------
    # Paths
    # -------------------------
    pdf_dir: Path = Field(
        default=PROJECT_ROOT / "documents",
        validation_alias="PDF_DIR",
    )

    faiss_index_dir: Path = Field(
        default=PROJECT_ROOT / "storage" / "faiss_index",
        validation_alias="FAISS_INDEX_DIR",
    )


    # -------------------------
    # Chunking
    # -------------------------
    chunk_size: int = Field(
        default=1000,
        validation_alias="CHUNK_SIZE",
    )

    chunk_overlap: int = Field(
        default=200,
        validation_alias="CHUNK_OVERLAP",
    )


    # -------------------------
    # Retrieval
    # -------------------------
    top_k: int = Field(
        default=4,
        validation_alias="TOP_K",
    )


    # -------------------------
    # Level 2 Enhancement
    # Retrieval Confidence Filtering
    # -------------------------
    min_retrieval_score: float = Field(
        default=0.3,
        validation_alias="MIN_RETRIEVAL_SCORE",
    )


    def ensure_directories(self) -> None:
        """
        Create required directories if they do not exist.
        """
        self.pdf_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.faiss_index_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


def get_settings() -> Settings:
    """
    Return application settings.
    """
    return Settings()
