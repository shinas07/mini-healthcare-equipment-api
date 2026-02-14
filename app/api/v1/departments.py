"""Department endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db_session
from app.api.response import success_response
from app.schemas.department import DepartmentCreate, DepartmentRead
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_department(
    payload: DepartmentCreate,
    db: AsyncSession = Depends(get_db_session),
):
    department = await DepartmentService(db).create_department(payload)
    data = DepartmentRead.model_validate(department).model_dump(mode="json")
    return success_response("Department created successfully", data=data).model_dump()


@router.get("")
async def list_departments(
    organization_id: int | None = Query(default=None, ge=1),
    db: AsyncSession = Depends(get_db_session),
):
    departments = await DepartmentService(db).list_departments(organization_id)
    data = [DepartmentRead.model_validate(item).model_dump(mode="json") for item in departments]
    return success_response("Departments fetched successfully", data=data).model_dump()
