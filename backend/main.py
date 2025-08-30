import os
from fastapi import FastAPI
from .routers import summarize, document_qa, learning_path


os.makedirs("docs", exist_ok=True)
os.makedirs("vector_store", exist_ok=True)

app = FastAPI(
    title="AI Microservices API",
    description="An API for various AI-powered tasks.",
    version="1.0.0"
)

app.include_router(summarize.router, prefix="/api", tags=["Summarization"])
app.include_router(document_qa.router, prefix="/api", tags=["Document Q&A"])
app.include_router(learning_path.router, prefix="/api", tags=["Learning Path"])

@app.get("/")
def read_root():
    return {"status": "API is running. Visit /docs for documentation."}