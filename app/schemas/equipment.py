"""Equipment request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.repositories.enums import EquipmentStatus


class EquipmentBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    manufacturer: str = Field(min_length=2, max_length=150)
    model_number: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=2, max_length=120)
    status: EquipmentStatus
    department_id: int = Field(ge=1)


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
