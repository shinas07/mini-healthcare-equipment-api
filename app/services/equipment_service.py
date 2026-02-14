"""Business logic for equipment operations."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import ConflictException, NotFoundException
from app.repositories.department import Department
from app.repositories.enums import EquipmentStatus
from app.repositories.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate


class EquipmentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def _get_department_or_none(self, department_id: int) -> Department | None:
        stmt = select(Department).where(Department.id == department_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def create_equipment(self, payload: EquipmentCreate) -> Equipment:
        department = await self._get_department_or_none(payload.department_id)
        if not department:
            raise NotFoundException("Department not found")

        duplicate_stmt = select(Equipment).where(
            Equipment.department_id == payload.department_id,
            func.lower(Equipment.name) == payload.name.strip().lower(),
            func.lower(Equipment.manufacturer) == payload.manufacturer.strip().lower(),
            func.lower(Equipment.model_number) == payload.model_number.strip().lower(),
        )
        duplicate = (await self.db.execute(duplicate_stmt)).scalar_one_or_none()
        if duplicate:
            raise ConflictException("Equipment already exists in this department")

        equipment = Equipment(
            name=payload.name.strip(),
            manufacturer=payload.manufacturer.strip(),
            model_number=payload.model_number.strip(),
            category=payload.category.strip(),
            status=payload.status,
            department_id=payload.department_id,
        )
        self.db.add(equipment)
        await self.db.commit()
        await self.db.refresh(equipment)
        return equipment

    async def get_equipment(self, equipment_id: int) -> Equipment:
        stmt = select(Equipment).where(Equipment.id == equipment_id)
        equipment = (await self.db.execute(stmt)).scalar_one_or_none()
        if not equipment:
            raise NotFoundException("Equipment not found")
        return equipment

    async def list_equipment(
        self,
        department_id: int | None,
        status: EquipmentStatus | None,
        page: int,
        page_size: int,
    ) -> tuple[list[Equipment], int]:
        stmt = select(Equipment)

        if department_id is not None:
            stmt = stmt.where(Equipment.department_id == department_id)
        if status is not None:
            stmt = stmt.where(Equipment.status == status)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_items = (await self.db.execute(count_stmt)).scalar_one()

        stmt = (
            stmt.order_by(Equipment.id.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = (await self.db.execute(stmt)).scalars().all()

        return list(items), int(total_items)

    async def update_equipment(self, equipment_id: int, payload: EquipmentUpdate) -> Equipment:
        equipment = await self.get_equipment(equipment_id)

        department = await self._get_department_or_none(payload.department_id)
        if not department:
            raise NotFoundException("Department not found")

        for key, value in payload.model_dump().items():
            if isinstance(value, str):
                value = value.strip()
            setattr(equipment, key, value)

        await self.db.commit()
        await self.db.refresh(equipment)
        return equipment
