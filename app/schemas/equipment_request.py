"""Equipment request schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.repositories.enums import EquipmentRequestStatus


class EquipmentRequestCreate(BaseModel):
    equipment_id: int = Field(ge=1)
    requested_by: str = Field(min_length=2, max_length=120)
    justification: str = Field(min_length=5, max_length=2000)
    priority: int = Field(ge=1, le=5)
    organization_id: int = Field(ge=1)


class EquipmentRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    equipment_id: int
    requested_by: str
    justification: str
    priority: int
    status: EquipmentRequestStatus
    organization_id: int
    created_at: datetime
