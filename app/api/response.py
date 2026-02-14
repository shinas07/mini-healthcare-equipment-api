"""Standard API response envelope helpers."""

from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: dict[str, Any] = Field(default_factory=dict)


def success_response(message: str, data: T | None = None) -> SuccessResponse[T]:
    """Build success response in required interview format."""
    return SuccessResponse(message=message, data=jsonable_encoder(data))


def error_response(message: str, errors: dict[str, Any] | None = None) -> ErrorResponse:
    """Build error response in required interview format."""
    return ErrorResponse(message=message, errors=errors or {})
