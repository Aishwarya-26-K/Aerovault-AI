"""
RAG Chain - Level 2 enhancement

Adds:
- retrieval confidence checking
- hallucination prevention
- source-aware answers
- confidence label for UI
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
                "confidence": 0,
                "confidence_label": "Low",
                "sources": []
            }


        # Confidence calculation

        best_score = min(
            item["score"]
            for item in results
        )

        confidence = round(
            max(0, 1 - (best_score / 10)),
            2
        )


        threshold = 0.35


        if confidence < threshold:

            return {
                "question": question,
                "answer":
                    "The information is not available in the provided document(s)",
                "confidence": confidence,
                "confidence_label":
                    self.get_confidence_label(confidence),
                "sources":
                    self.get_sources(results)
            }


        context = "\n\n".join(
            item["text"]
            for item in results
        )


        prompt = f"""
You are an aviation assistant.

Answer only using the provided aviation document context.

Do not use outside knowledge.

If the information is missing, say:
"I do not have enough information."

Context:

{context}


Question:

{question}


Answer:
"""


        response = self.llm.invoke(prompt)


        return {
            "question": question,
            "answer": response.content.strip(),
            "confidence": confidence,
            "confidence_label":
                self.get_confidence_label(confidence),
            "sources":
                self.get_sources(results)
        }



    def get_sources(self, results):

        unique = []

        seen = set()


        for item in results:

            key = (
                item["filename"],
                item["page"]
            )

            if key not in seen:

                unique.append(
                    {
                        "file": item["filename"],
                        "page": item["page"]
                    }
                )

                seen.add(key)


        return unique



    def get_confidence_label(self, confidence):

        if confidence >= 0.75:
            return "High"

        elif confidence >= 0.50:
            return "Medium"

        else:
            return "Low"