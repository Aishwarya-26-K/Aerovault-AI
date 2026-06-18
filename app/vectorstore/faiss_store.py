"""
Build, persist, and query a FAISS vector index.

LangChain saves two files under storage/faiss_index/:
  - index.faiss  : the vector index (fast similarity search)
  - index.pkl    : the chunk text + metadata aligned with each vector
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

INDEX_FILES = ("index.faiss", "index.pkl")


def index_exists(index_dir: Path) -> bool:
    """Return True if a previously saved FAISS index is present."""
    return all((index_dir / name).exists() for name in INDEX_FILES)


def build_and_save_index(
    documents: list[Document],
    embeddings: Embeddings,
    index_dir: Path,
) -> FAISS:
    """
    Embed all documents, build a FAISS index, and save it to disk.

    This is the expensive step — run once after ingestion, then reload
    the saved index for searches.
    """
    if not documents:
        raise ValueError("Cannot build FAISS index from an empty document list.")

    index_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Embedding {len(documents)} chunks (this may take several minutes)...")

    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(str(index_dir))

    print(f"  Saved FAISS index to {index_dir}")
    return vectorstore


def load_index(embeddings: Embeddings, index_dir: Path) -> FAISS:
    """Load a FAISS index previously saved with build_and_save_index."""
    if not index_exists(index_dir):
        raise FileNotFoundError(
            f"No FAISS index found in {index_dir}. "
            "Run: python scripts/test_vector_search.py --build"
        )

    return FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def search_similar(
    vectorstore: FAISS,
    query: str,
    top_k: int = 4,
) -> list[tuple[Document, float]]:
    """
    Find the top_k chunks most similar to the query.

    Returns (Document, score) pairs. Lower score = closer match with L2 distance
    on normalized embeddings (LangChain default for this setup).
    """
    return vectorstore.similarity_search_with_score(query, k=top_k)
