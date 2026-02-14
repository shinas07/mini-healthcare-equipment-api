import pytest
from httpx import AsyncClient

from app.core.config import settings


def _path(path: str) -> str:
    prefix = settings.api_prefix.rstrip("/")
    return f"{prefix}{path}" if prefix else path


async def _create_department(client: AsyncClient, name: str, organization_id: int) -> dict:
    response = await client.post(
        _path("/departments"),
        json={"name": name, "organization_id": organization_id},
    )
    assert response.status_code == 201
    return response.json()["data"]


async def _create_equipment(
    client: AsyncClient,
    *,
    department_id: int,
    status: str,
    name: str,
) -> dict:
    response = await client.post(
        _path("/equipment"),
        json={
            "name": name,
            "manufacturer": "GE",
            "model_number": "M-1",
            "category": "Monitor",
            "status": status,
            "department_id": department_id,
        },
    )
    assert response.status_code == 201
    return response.json()["data"]


@pytest.mark.anyio
async def test_decommissioned_equipment_cannot_be_requested(client: AsyncClient) -> None:
    department = await _create_department(client, "ICU", 10)
    equipment = await _create_equipment(
        client,
        department_id=department["id"],
        status="decommissioned",
        name="Ventilator-X",
    )

    response = await client.post(
        _path("/equipment-requests"),
        json={
            "equipment_id": equipment["id"],
            "requested_by": "Dr Arun",
            "justification": "Critical usage required",
            "priority": 3,
            "organization_id": 10,
        },
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "Decommissioned equipment cannot be requested"


@pytest.mark.anyio
async def test_only_pending_request_can_be_approved_once(client: AsyncClient) -> None:
    department = await _create_department(client, "ER", 20)
    equipment = await _create_equipment(
        client,
        department_id=department["id"],
        status="available",
        name="Defibrillator-Z",
    )

    create_request = await client.post(
        _path("/equipment-requests"),
        json={
            "equipment_id": equipment["id"],
            "requested_by": "Nurse Mia",
            "justification": "Immediate emergency readiness",
            "priority": 2,
            "organization_id": 20,
        },
    )
    assert create_request.status_code == 201

    request_id = create_request.json()["data"]["id"]

    first_approve = await client.patch(_path(f"/equipment-requests/{request_id}/approve"))
    assert first_approve.status_code == 200
    assert first_approve.json()["data"]["status"] == "approved"

    second_approve = await client.patch(_path(f"/equipment-requests/{request_id}/approve"))
    assert second_approve.status_code == 400
    assert second_approve.json()["message"] == "Only pending requests can be approved"
