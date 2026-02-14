"""Equipment request endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.api.response import success_response
from app.schemas.equipment_request import EquipmentRequestCreate, EquipmentRequestRead
from app.services.equipment_request_service import EquipmentRequestService

router = APIRouter(prefix="/equipment-requests", tags=["Equipment Requests"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_equipment_request(
    payload: EquipmentRequestCreate,
    db: AsyncSession = Depends(get_db_session),
):
    request = await EquipmentRequestService(db).create_request(payload)
    data = EquipmentRequestRead.model_validate(request).model_dump(mode="json")
    return success_response("Equipment request created successfully", data).model_dump()


@router.patch("/{request_id}/approve")
async def approve_equipment_request(
    request_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    request = await EquipmentRequestService(db).approve_request(request_id)
    data = EquipmentRequestRead.model_validate(request).model_dump(mode="json")
    return success_response("Equipment request approved successfully", data).model_dump()


@router.get("")
async def list_equipment_requests(
    organization_id: int = Query(..., ge=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db_session),
):
    items, total_items = await EquipmentRequestService(db).list_by_organization(
        organization_id=organization_id,
        page=page,
        page_size=page_size,
    )
    total_pages = (total_items + page_size - 1) // page_size

    data = {
        "items": [EquipmentRequestRead.model_validate(item).model_dump(mode="json") for item in items],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        },
    }
    return success_response("Equipment requests fetched successfully", data).model_dump()
