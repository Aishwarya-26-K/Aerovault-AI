from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.chain import RAGChain
from app.retrieval.retriever import Retriever


router = APIRouter()


retriever = Retriever()
rag = RAGChain(retriever)


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(request: QuestionRequest):

    answer = rag.ask(request.question)

    return {
        "question": request.question,
        "answer": answer
    }