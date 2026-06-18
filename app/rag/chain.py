from app.llm.generator import get_llm


class RAGChain:

    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = get_llm()


    def ask(self, question: str):

        results = self.retriever.search(question)

        context_parts = []

        for item in results:

            # Case 1: (Document, score)
            if isinstance(item, tuple):
                doc = item[0]
                context_parts.append(doc.page_content)

            # Case 2: LangChain Document
            elif hasattr(item, "page_content"):
                context_parts.append(item.page_content)

            # Case 3: dictionary
            elif isinstance(item, dict):
                context_parts.append(
                    item.get("content")
                    or item.get("text")
                    or str(item)
                )


        context = "\n\n".join(context_parts)


        prompt = f"""
You are an aviation assistant.

Answer only using the provided context.

If the answer is not present in the context, say:
Information not available in provided documents.

Context:

{context}

Question:

{question}
"""


        response = self.llm.invoke(prompt)

        return response.content