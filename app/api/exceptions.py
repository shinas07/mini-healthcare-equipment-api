"""Central exception classes and FastAPI handlers."""

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.response import error_response
from app.core.config import settings


class APIException(Exception):
    """Application-level exception for consistent API errors."""

    def __init__(
        self,
        status_code: int,
        message: str,
        errors: dict[str, Any] | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors or {}
        super().__init__(message)


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(404, message)


class BadRequestException(APIException):
    def __init__(self, message: str = "Bad request") -> None:
        super().__init__(400, message)


class ConflictException(APIException):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(409, message)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global handlers once during app startup."""

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):  # noqa: ARG001
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.message, exc.errors).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # noqa: ARG001
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content=error_response("Validation error", {"details": exc.errors()}).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):  # noqa: ARG001
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(str(exc.detail), {}).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):  # noqa: ARG001
        details = {"detail": str(exc)} if settings.debug else {}
        return JSONResponse(
            status_code=500,
            content=error_response("Internal server error", details).model_dump(),
        )
