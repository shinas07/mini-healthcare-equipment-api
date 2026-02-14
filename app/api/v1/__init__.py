"""Versioned API router composition."""

from fastapi import APIRouter

from app.api.v1.departments import router as departments_router
from app.api.v1.equipment import router as equipment_router
from app.api.v1.equipment_requests import router as equipment_requests_router

api_router = APIRouter()
api_router.include_router(departments_router)
api_router.include_router(equipment_router)
api_router.include_router(equipment_requests_router)
