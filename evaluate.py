import json
from pathlib import Path

from app.rag.chain import RAGChain
from app.retrieval.retriever import Retriever


QUESTIONS_FILE = Path("evaluation/questions.json")
RESULT_FILE = Path("evaluation/results.json")


def main():

    retriever = Retriever()
    rag = RAGChain(retriever)

    questions = json.loads(
        QUESTIONS_FILE.read_text(
            encoding="utf-8"
        )
    )

    if RESULT_FILE.exists():
        results = json.loads(
            RESULT_FILE.read_text(
                encoding="utf-8"
            )
        )
        completed = {x["id"] for x in results}
    else:
        results = []
        completed = set()


    for item in questions:

        if item["id"] in completed:
            continue

        print(
            f"Testing {item['id']}: {item['question']}"
        )

        try:

            response = rag.ask(
                item["question"]
            )

            results.append(
                {
                    "id": item["id"],
                    "question": item["question"],
                    "type": item["type"],
                    "confidence": response["confidence"],
                    "label": response["confidence_label"],
                    "answer": response["answer"]
                }
            )


            RESULT_FILE.write_text(
                json.dumps(
                    results,
                    indent=2
                ),
                encoding="utf-8"
            )


        except Exception as e:

            print(
                "Stopped because:",
                e
            )
            break


    print(
        f"Completed {len(results)}/50"
    )


if __name__ == "__main__":
    main()