from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings


def get_llm():

    settings = get_settings()

    if not settings.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY missing. Add it to .env"
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.google_api_key,
        temperature=0,
    )