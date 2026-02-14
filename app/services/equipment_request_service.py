"""Business logic for equipment request workflow."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import BadRequestException, ConflictException, NotFoundException
from app.repositories.department import Department
from app.repositories.enums import EquipmentRequestStatus, EquipmentStatus
from app.repositories.equipment import Equipment
from app.repositories.equipment_request import EquipmentRequest
from app.schemas.equipment_request import EquipmentRequestCreate


class EquipmentRequestService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def _get_equipment_or_none(self, equipment_id: int) -> Equipment | None:
        stmt = select(Equipment).where(Equipment.id == equipment_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def _get_department_or_none(self, department_id: int) -> Department | None:
        stmt = select(Department).where(Department.id == department_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def _get_request_or_none(self, request_id: int) -> EquipmentRequest | None:
        stmt = select(EquipmentRequest).where(EquipmentRequest.id == request_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

    async def create_request(self, payload: EquipmentRequestCreate) -> EquipmentRequest:
        equipment = await self._get_equipment_or_none(payload.equipment_id)
        if not equipment:
            raise NotFoundException("Equipment not found")

        if equipment.status == EquipmentStatus.DECOMMISSIONED:
            raise BadRequestException("Decommissioned equipment cannot be requested")

        duplicate_stmt = select(EquipmentRequest).where(
            EquipmentRequest.equipment_id == payload.equipment_id,
            EquipmentRequest.organization_id == payload.organization_id,
            func.lower(EquipmentRequest.requested_by) == payload.requested_by.strip().lower(),
            EquipmentRequest.status == EquipmentRequestStatus.PENDING,
        )
        duplicate = (await self.db.execute(duplicate_stmt)).scalar_one_or_none()
        if duplicate:
            raise ConflictException("Pending request already exists for this equipment")

        department = await self._get_department_or_none(equipment.department_id)
        if not department:
            raise NotFoundException("Department not found for equipment")

        if department.organization_id != payload.organization_id:
            raise BadRequestException("organization_id does not match equipment organization")

        request = EquipmentRequest(
            equipment_id=payload.equipment_id,
            requested_by=payload.requested_by.strip(),
            justification=payload.justification.strip(),
            priority=payload.priority,
            organization_id=payload.organization_id,
        )
        self.db.add(request)
        await self.db.commit()
        await self.db.refresh(request)
        return request

    async def approve_request(self, request_id: int) -> EquipmentRequest:
        request = await self._get_request_or_none(request_id)
        if not request:
            raise NotFoundException("Equipment request not found")

        if request.status != EquipmentRequestStatus.PENDING:
            raise BadRequestException("Only pending requests can be approved")

        request.status = EquipmentRequestStatus.APPROVED
        await self.db.commit()
        await self.db.refresh(request)
        return request

    async def list_by_organization(
        self,
        organization_id: int,
        page: int,
        page_size: int,
    ) -> tuple[list[EquipmentRequest], int]:
        base_stmt = select(EquipmentRequest).where(
            EquipmentRequest.organization_id == organization_id
        )
        total_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_items = (await self.db.execute(total_stmt)).scalar_one()

        stmt = (
            base_stmt.order_by(EquipmentRequest.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = (await self.db.execute(stmt)).scalars().all()

        return list(items), int(total_items)
