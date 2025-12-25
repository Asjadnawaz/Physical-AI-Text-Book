from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .v1 import chat, sessions, search, embeddings
from ..config.settings import settings


def create_app():
    app = FastAPI(
        title="RAG Chatbot API",
        description="API for the RAG Chatbot integration with the Physical AI & Humanoid Robotics textbook",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
    app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
    app.include_router(search.router, prefix="/api/v1", tags=["search"])
    app.include_router(embeddings.router, prefix="/api/v1", tags=["embeddings"])

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "RAG Chatbot API"}

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG
    )