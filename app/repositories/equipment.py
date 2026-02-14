from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.repositories.enums import EquipmentStatus


class Equipment(Base):
    __tablename__ = "equipment"

    __table_args__ = (
        Index("ix_equipment_department_status", "department_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(150), nullable=False)
    model_number: Mapped[str] = mapped_column(String(120), nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[EquipmentStatus] = mapped_column(
        SqlEnum(EquipmentStatus, name="equipment_status_enum", native_enum=False),
        nullable=False,
        default=EquipmentStatus.AVAILABLE,
        server_default=EquipmentStatus.AVAILABLE.value,
        index=True,
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    department = relationship("Department", back_populates="equipment_items")
    equipment_requests = relationship("EquipmentRequest", back_populates="equipment")
