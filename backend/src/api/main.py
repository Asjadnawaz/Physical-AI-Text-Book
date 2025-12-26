from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .v1 import chat, sessions, search, embeddings
from ..config.settings import settings
from .exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from .middleware import TextbookContentValidationMiddleware
from .rate_limiter import rate_limit_middleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def create_app():
    app = FastAPI(
        title="RAG Chatbot API",
        description="API for the RAG Chatbot integration with the Physical AI & Humanoid Robotics textbook",
        version="1.0.0"
    )

    # Add exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Add rate limiting middleware first
    app.middleware("http")(rate_limit_middleware)

    # Add custom middleware for textbook content validation
    app.add_middleware(TextbookContentValidationMiddleware)

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