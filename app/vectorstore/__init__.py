"""FAISS vector store for aviation document chunks."""

from app.vectorstore.faiss_store import (
    build_and_save_index,
    index_exists,
    load_index,
    search_similar,
)

__all__ = ["build_and_save_index", "index_exists", "load_index", "search_similar"]
