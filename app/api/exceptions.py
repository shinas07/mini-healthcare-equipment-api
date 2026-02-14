from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.response import error_response


class APIException(Exception):
    def __init__(self, status_code: int, message: str, errors: Any | None = None) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors or {}


class NotFoundException(APIException):
    def __init__(self, message: str = "Resource not found", errors: Any | None = None) -> None:
        super().__init__(404, message, errors)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(APIException)
    async def handle_api_exception(request: Request, exc: APIException) -> JSONResponse:  # noqa: ARG001
        return JSONResponse(status_code=exc.status_code, content=error_response(exc.message, exc.errors))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:  # noqa: ARG001
        return JSONResponse(status_code=422, content=error_response("Validation error", exc.errors()))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
        return JSONResponse(status_code=500, content=error_response("Internal server error", {"detail": str(exc)}))
