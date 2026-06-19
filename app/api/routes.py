from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.chain import RAGChain
from app.retrieval.retriever import Retriever


router = APIRouter()


# Create components once
retriever = Retriever()
rag = RAGChain(retriever)


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_question(request: QuestionRequest):

    result = rag.ask(request.question)

    return result