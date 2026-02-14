from typing import Any, Generic, TypeVar

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
    return SuccessResponse(message=message, data=data)


def error_response(message: str, errors: dict[str, Any] | None = None) -> ErrorResponse:
    return ErrorResponse(message=message, errors=errors or {})
