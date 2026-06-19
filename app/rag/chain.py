"""
RAG Chain - Level 2 enhancement

Adds:
- retrieval confidence checking
- hallucination prevention
- source-aware answers
"""

from app.config import get_settings
from app.llm.generator import get_llm


class RAGChain:

    def __init__(self, retriever):

        self.settings = get_settings()
        self.retriever = retriever
        self.llm = get_llm()


    def ask(self, question: str):

        results = self.retriever.search(question)


        if not results:
            return {
                "question": question,
                "answer": "No relevant information found.",
                "sources": [],
                "confidence": 0
            }


        # FAISS distance score:
        # lower distance = better match
        best_score = min(
            item["score"]
            for item in results
        )


        # convert distance to confidence
        confidence = round(
            1 / (1 + best_score),
            2
        )


        # Level 2 threshold
        threshold = 0.35


        if confidence < threshold:

            return {
                "question": question,
                "answer":
                    "I could not find enough information in the provided aviation documents.",
                "sources": [
                    {
                        "file": item["filename"],
                        "page": item["page"]
                    }
                    for item in results
                ],
                "confidence": confidence
            }


        context = "\n\n".join(
            item["text"]
            for item in results
        )


        prompt = f"""
You are an aviation assistant.

Answer ONLY from the context.
If information is missing, say so.

Context:
{context}


Question:
{question}

Answer:
"""


        response = self.llm.invoke(prompt)


        return {
            "question": question,
            "answer": response.content,
            "sources": [
                {
                    "file": item["filename"],
                    "page": item["page"]
                }
                for item in results
            ],
            "confidence": confidence
        }