from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="AeroVault AI",
    description="Aviation RAG Assistant",
    version="1.0"
)


app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
def root():
    return {
        "status": "AeroVault AI running"
    }