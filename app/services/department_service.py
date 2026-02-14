"""Business logic for department operations."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ConflictException
from app.repositories.department import Department
from app.schemas.department import DepartmentCreate


class DepartmentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_department(self, payload: DepartmentCreate) -> Department:
        duplicate_stmt = select(Department).where(
            Department.organization_id == payload.organization_id,
            func.lower(Department.name) == payload.name.strip().lower(),
        )
        duplicate = (await self.db.execute(duplicate_stmt)).scalar_one_or_none()
        if duplicate:
            raise ConflictException("Department already exists")

        department = Department(
            name=payload.name.strip(),
            organization_id=payload.organization_id,
        )
        self.db.add(department)
        await self.db.commit()
        await self.db.refresh(department)
        return department

    async def get_department(self, department_id: int) -> Department | None:
        stmt = select(Department).where(Department.id == department_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def list_departments(self, organization_id: int | None = None) -> list[Department]:
        stmt = select(Department).order_by(Department.id.asc())
        if organization_id is not None:
            stmt = stmt.where(Department.organization_id == organization_id)
        return list((await self.db.execute(stmt)).scalars().all())
