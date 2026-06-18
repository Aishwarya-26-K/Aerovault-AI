"""
Phase 2 test script — load PDFs, chunk them, print samples.

Run from project root:
    python scripts/test_ingestion.py

Optional: show more sample chunks
    python scripts/test_ingestion.py --samples 5
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.config import get_settings
from app.ingestion.chunker import chunk_documents
from app.ingestion.pdf_loader import load_all_pdfs


def preview_text(text: str, max_chars: int = 300) -> str:
    """Show a readable snippet without flooding the terminal."""
    cleaned = " ".join(text.split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 3] + "..."


def main() -> None:
    parser = argparse.ArgumentParser(description="Test PDF ingestion (Phase 2)")
    parser.add_argument(
        "--samples",
        type=int,
        default=3,
        help="Number of sample chunks to display (default: 3)",
    )
    args = parser.parse_args()

    settings = get_settings()
    settings.ensure_directories()

    print("=" * 70)
    print("Phase 2 — PDF Ingestion Test")
    print("=" * 70)
    print(f"PDF folder: {settings.pdf_dir}")
    print(f"Chunk size: {settings.chunk_size} | Overlap: {settings.chunk_overlap}")
    print()

    pdf_files = sorted(settings.pdf_dir.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF file(s)")
    print("\nLoading pages...")
    pages = load_all_pdfs(settings.pdf_dir)

    print(f"\nTotal pages loaded (non-empty): {len(pages)}")

    chunks = chunk_documents(
        pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    print(f"Total chunks created: {len(chunks)}")

    pages_per_file = Counter(doc.metadata["filename"] for doc in pages)
    chunks_per_file = Counter(chunk.metadata["filename"] for chunk in chunks)

    print("\nBreakdown by PDF:")
    for filename in sorted(pages_per_file):
        print(
            f"  {filename}: {pages_per_file[filename]} pages -> "
            f"{chunks_per_file[filename]} chunks"
        )

    sample_count = min(args.samples, len(chunks))
    print(f"\nSample chunks (showing {sample_count}):")
    print("-" * 70)
    for index, chunk in enumerate(chunks[:sample_count], start=1):
        filename = chunk.metadata.get("filename", "unknown")
        page = chunk.metadata.get("page", "?")
        print(f"[Chunk {index}] {filename} | page {page}")
        print(preview_text(chunk.page_content))
        print("-" * 70)

    print("\nPhase 2 ingestion test complete.")
    print("Next step (Phase 3): embed these chunks and store them in FAISS.")
    print("=" * 70)


if __name__ == "__main__":
    main()
