"""
Load aviation PDFs from disk, one LangChain Document per page.

Each page keeps metadata needed later for citations:
  - filename: PDF file name (e.g. "Meteorology.pdf")
  - page: 1-based page number inside that PDF
"""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf_pages(pdf_path: Path) -> list[Document]:
    """Extract text from a single PDF, one document per non-empty page."""
    loader = PyPDFLoader(str(pdf_path))
    raw_pages = loader.load()
    filename = pdf_path.name

    pages: list[Document] = []
    for doc in raw_pages:
        text = doc.page_content.strip()
        if not text:
            continue

        # PyPDFLoader uses 0-based page indexes; humans expect 1-based page numbers.
        raw_page = doc.metadata.get("page", 0)
        page_number = int(raw_page) + 1

        pages.append(
            Document(
                page_content=text,
                metadata={
                    "filename": filename,
                    "page": page_number,
                },
            )
        )

    return pages


def load_all_pdfs(pdf_dir: Path) -> list[Document]:
    """Load every *.pdf in pdf_dir and return all page documents."""
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {pdf_dir}")

    all_pages: list[Document] = []
    for pdf_path in pdf_files:
        pages = load_pdf_pages(pdf_path)
        all_pages.extend(pages)
        print(f"  Loaded {len(pages):>4} pages from {pdf_path.name}")

    return all_pages
