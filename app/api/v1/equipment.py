"""Equipment endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.api.response import success_response
from app.repositories.enums import EquipmentStatus
from app.schemas.ai import AIAssessmentInput
from app.schemas.equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate
from app.services.ai_assessment_service import AIAssessmentService
from app.services.equipment_service import EquipmentService

router = APIRouter(prefix="/equipment", tags=["Equipment"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_equipment(
    payload: EquipmentCreate,
    db: AsyncSession = Depends(get_db_session),
):
    equipment = await EquipmentService(db).create_equipment(payload)
    data = EquipmentRead.model_validate(equipment).model_dump(mode="json")
    return success_response("Equipment created successfully", data).model_dump()


@router.get("/{equipment_id}")
async def get_equipment(
    equipment_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    equipment = await EquipmentService(db).get_equipment(equipment_id)
    data = EquipmentRead.model_validate(equipment).model_dump(mode="json")
    return success_response("Equipment fetched successfully", data).model_dump()


@router.get("")
async def list_equipment(
    department_id: int | None = Query(default=None, ge=1),
    status: EquipmentStatus | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db_session),
):
    items, total_items = await EquipmentService(db).list_equipment(
        department_id=department_id,
        status=status,
        page=page,
        page_size=page_size,
    )
    total_pages = (total_items + page_size - 1) // page_size

    data = {
        "items": [EquipmentRead.model_validate(item).model_dump(mode="json") for item in items],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        },
    }
    return success_response("Equipment list fetched successfully", data).model_dump()


@router.put("/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    payload: EquipmentUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    equipment = await EquipmentService(db).update_equipment(equipment_id, payload)
    data = EquipmentRead.model_validate(equipment).model_dump(mode="json")
    return success_response("Equipment updated successfully", data).model_dump()


@router.post("/{equipment_id}/ai-assessment")
async def ai_assessment(
    equipment_id: int,
    payload: AIAssessmentInput,
    db: AsyncSession = Depends(get_db_session),
):
    equipment = await EquipmentService(db).get_equipment(equipment_id)
    assessment = AIAssessmentService().generate(equipment, payload)
    return success_response(
        "AI assessment generated successfully",
        assessment.model_dump(mode="json"),
    ).model_dump()
