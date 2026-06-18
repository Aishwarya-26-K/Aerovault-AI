"""
Retriever module.

Loads the saved FAISS index and searches for
the most relevant aviation document chunks.
"""

from app.config import get_settings
from app.embeddings.embedder import get_embeddings
from app.vectorstore.faiss_store import load_index


class Retriever:

    def __init__(self):
        # Load project settings
        settings = get_settings()

        # Load embedding model
        embeddings = get_embeddings(settings.embedding_model)

        # Load existing FAISS vector database
        self.vectorstore = load_index(
            embeddings=embeddings,
            index_dir=settings.faiss_index_dir,
        )

        # Number of chunks to retrieve
        self.top_k = settings.top_k


    def search(self, query: str):
        """
        Search FAISS for relevant chunks.

        Returns:
        text + filename + page + similarity score
        """

        results = self.vectorstore.similarity_search_with_score(
            query,
            k=self.top_k,
        )

        retrieved_chunks = []

        for doc, score in results:
            retrieved_chunks.append(
                {
                    "text": doc.page_content,
                    "filename": doc.metadata.get("filename"),
                    "page": doc.metadata.get("page"),
                    "score": float(score),
                }
            )

        return retrieved_chunks