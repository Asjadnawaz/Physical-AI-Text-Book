from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for HTTP exceptions
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "http_exception",
                "message": str(exc.detail) if hasattr(exc, 'detail') else "HTTP Exception occurred",
                "status_code": exc.status_code
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for request validation errors
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler for unhandled exceptions
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "internal_error",
                "message": "An internal server error occurred"
            }
        }
    )