print("STARTING RETRIEVAL TEST")

from app.retrieval.retriever import Retriever

print("IMPORT OK")

retriever = Retriever()

print("RETRIEVER LOADED")

question = "What is wind shear?"

results = retriever.search(question)

print("SEARCH DONE")


for r in results:
    print("----------------")
    print("File:", r["filename"])
    print("Page:", r["page"])
    print("Score:", r["score"])
    print(r["text"][:300])