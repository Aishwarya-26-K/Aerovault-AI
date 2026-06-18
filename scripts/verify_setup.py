"""
Phase 1 verification script.

Run after creating your virtual environment and installing requirements:
    python scripts/verify_setup.py

This does NOT test RAG yet — only that the foundation is ready.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `from app.config import ...` when run from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def check_python_version() -> None:
    major, minor = sys.version_info[:2]
    print(f"Python version: {major}.{minor}.{sys.version_info.micro}")
    if major < 3 or (major == 3 and minor < 10):
        raise SystemExit("ERROR: Python 3.10 or newer is required.")


def check_imports() -> None:
    """Import key libraries once so we know dependencies installed correctly."""
    modules = [
        ("dotenv", "python-dotenv"),
        ("pydantic_settings", "pydantic-settings"),
        ("langchain", "langchain"),
        ("langchain_community", "langchain-community"),
        ("sentence_transformers", "sentence-transformers"),
        ("faiss", "faiss-cpu"),
        ("pypdf", "pypdf"),
        ("fastapi", "fastapi"),
    ]
    print("\nChecking imports:")
    for module_name, package_name in modules:
        try:
            __import__(module_name)
            print(f"  OK  {package_name}")
        except ImportError as exc:
            raise SystemExit(f"  FAIL {package_name}: {exc}") from exc


def check_config() -> None:
    from app.config import PROJECT_ROOT, get_settings

    settings = get_settings()
    settings.ensure_directories()

    print("\nConfiguration:")
    print(f"  Project root:     {PROJECT_ROOT}")
    print(f"  PDF directory:    {settings.pdf_dir}")
    print(f"  FAISS index dir:  {settings.faiss_index_dir}")
    print(f"  Embedding model:  {settings.embedding_model}")
    print(f"  LLM provider:     {settings.llm_provider}")
    print(f"  Chunk size/over:  {settings.chunk_size} / {settings.chunk_overlap}")
    print(f"  Top-K retrieval:  {settings.top_k}")

    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        print(f"  .env file:        found at {env_file}")
    else:
        print("  .env file:        NOT FOUND (copy .env.example to .env when ready)")

    pdf_count = len(list(settings.pdf_dir.glob("*.pdf")))
    print(f"  PDFs in documents: {pdf_count} (add your aviation PDFs here in Phase 2)")


def main() -> None:
    print("=" * 60)
    print("Aviation RAG Assistant — Phase 1 Setup Verification")
    print("=" * 60)
    check_python_version()
    check_imports()
    check_config()
    print("\nPhase 1 setup looks good. Ready for Phase 2 (PDF ingestion).")
    print("=" * 60)


if __name__ == "__main__":
    main()
