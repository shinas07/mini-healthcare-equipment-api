from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.repositories.enums import EquipmentRequestStatus


class EquipmentRequest(Base):
    __tablename__ = "equipment_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    requested_by: Mapped[str] = mapped_column(String(120), nullable=False)
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[EquipmentRequestStatus] = mapped_column(
        SqlEnum(EquipmentRequestStatus, name="equipment_request_status_enum", native_enum=False),
        nullable=False,
        default=EquipmentRequestStatus.PENDING,
        server_default=EquipmentRequestStatus.PENDING.value,
    )
    organization_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    equipment = relationship("Equipment", back_populates="equipment_requests")