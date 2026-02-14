"""Application entrypoint."""

from fastapi import FastAPI

from app.api.exceptions import register_exception_handlers
from app.api.response import SuccessResponse, success_response
from app.api.v1 import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health", response_model=SuccessResponse[dict[str, str]])
async def health() -> SuccessResponse[dict[str, str]]:
    """Basic readiness endpoint."""
    return success_response(
        message="Service is healthy",
        data={"status": "ok", "environment": settings.app_env},
    )
