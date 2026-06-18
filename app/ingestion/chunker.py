"""
Split page-level documents into smaller chunks for retrieval.

Why chunk?
- A full PDF page can exceed the LLM context window.
- Smaller chunks improve retrieval precision (the retriever finds tighter matches).
- Overlap prevents sentences from being cut in half at chunk boundaries.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[Document]:
    """
    Split documents into overlapping chunks.

    Metadata (filename, page) is copied to every chunk so citations still work
    after splitting.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        # Try to split on paragraph breaks first, then lines, then words.
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(documents)
