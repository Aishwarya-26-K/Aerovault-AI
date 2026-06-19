from app.config import get_settings
from app.ingestion.pdf_loader import load_all_pdfs
from app.ingestion.chunker import chunk_documents
from app.embeddings.embedder import get_embeddings
from app.vectorstore.faiss_store import build_and_save_index


def main():

    settings = get_settings()

    print("Loading PDFs...")
    pages = load_all_pdfs(settings.pdf_dir)

    print(f"Loaded {len(pages)} pages")

    print("Creating chunks...")
    chunks = chunk_documents(
        pages,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    print(f"Created {len(chunks)} chunks")

    print("Loading embedding model...")
    embeddings = get_embeddings(settings.embedding_model)

    print("Building FAISS index...")
    build_and_save_index(
        documents=chunks,
        embeddings=embeddings,
        index_dir=settings.faiss_index_dir,
    )

    print("✅ FAISS rebuild completed")


if __name__ == "__main__":
    main()