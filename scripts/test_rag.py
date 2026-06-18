from app.retrieval.retriever import Retriever
from app.rag.chain import RAGChain


print("STARTING RAG TEST")


retriever = Retriever()

rag = RAGChain(retriever)


answer = rag.ask(
    "What is wind?"
)


print("\nANSWER:")
print(answer)