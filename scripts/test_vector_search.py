"""
Phase 3 test script — build FAISS index and search similar chunks.

Build index (ingest PDFs + embed + save):
    python scripts/test_vector_search.py --build

Search with a custom question:
    python scripts/test_vector_search.py --query "What is wind shear?"

Run default sample queries against an existing index:
    python scripts/test_vector_search.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.embeddings.embedder import get_embeddings
from app.ingestion.chunker import chunk_documents
from app.ingestion.pdf_loader import load_all_pdfs
from app.vectorstore.faiss_store import (
    build_and_save_index,
    index_exists,
    load_index,
    search_similar,
)

DEFAULT_QUERIES = [
    "What is wind shear?",
    "How is center of gravity calculated for an aircraft?",
    "What are the VFR weather minimums?",
]


def preview_text(text: str, max_chars: int = 250) -> str:
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 3] + "..."


def run_searches(vectorstore, queries: list[str], top_k: int) -> None:
    for query in queries:
        print("\n" + "=" * 70)
        print(f"Query: {query}")
        print("=" * 70)

        results = search_similar(vectorstore, query, top_k=top_k)
        if not results:
            print("No results found.")
            continue

        for rank, (doc, score) in enumerate(results, start=1):
            filename = doc.metadata.get("filename", "unknown")
            page = doc.metadata.get("page", "?")
            print(f"\n[{rank}] score={score:.4f} | {filename} | page {page}")
            print(preview_text(doc.page_content))


def build_index(settings) -> None:
    print("Step 1/3 — Loading PDFs and chunking...")
    pages = load_all_pdfs(settings.pdf_dir)
    chunks = chunk_documents(
        pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    print(f"  Total chunks: {len(chunks)}")

    print("\nStep 2/3 — Loading embedding model...")
    embeddings = get_embeddings(settings.embedding_model)
    print(f"  Model: {settings.embedding_model}")

    print("\nStep 3/3 — Building and saving FAISS index...")
    build_and_save_index(chunks, embeddings, settings.faiss_index_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Test embeddings + FAISS (Phase 3)")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Ingest PDFs, embed chunks, and save FAISS index",
    )
    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        help="Search query (can be repeated). Omit to use sample queries.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of results per query (default: from config TOP_K)",
    )
    args = parser.parse_args()

    settings = get_settings()
    settings.ensure_directories()
    top_k = args.top_k or settings.top_k

    print("=" * 70)
    print("Phase 3 — Embeddings + FAISS Test")
    print("=" * 70)
    print(f"Embedding model: {settings.embedding_model}")
    print(f"FAISS index dir: {settings.faiss_index_dir}")
    print(f"Top-K:           {top_k}")

    if args.build:
        build_index(settings)
    elif not index_exists(settings.faiss_index_dir):
        raise SystemExit(
            "\nNo saved index found. Build one first:\n"
            "  python scripts/test_vector_search.py --build"
        )

    print("\nLoading FAISS index...")
    embeddings = get_embeddings(settings.embedding_model)
    vectorstore = load_index(embeddings, settings.faiss_index_dir)
    print("  Index loaded.")

    queries = args.queries if args.queries else DEFAULT_QUERIES
    if not args.build and not args.queries:
        print("\nRunning default sample queries (use --query to test your own):")

    run_searches(vectorstore, queries, top_k=top_k)

    print("\n" + "=" * 70)
    print("Phase 3 vector search test complete.")
    print("Next step (Phase 4): wrap retrieval in a reusable retriever module.")
    print("=" * 70)


if __name__ == "__main__":
    main()
