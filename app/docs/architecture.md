# Architecture Overview

## Layers
- API layer (`app/api/v1/*`): request/response transport and validation wiring.
- Service layer (`app/services/*`): business rules and orchestration.
- Repository/Model layer (`app/repositories/*`): SQLAlchemy ORM models.
- Schema layer (`app/schemas/*`): Pydantic input/output contracts.

## Key Rules
- Department name must be unique per organization (service check).
- Equipment identity is deduplicated within a department (service check).
- Decommissioned equipment cannot be requested.
- Only pending equipment requests can be approved.

## Error Handling
All errors use centralized `APIException` handlers and return a consistent envelope.

## AI Endpoint
`POST /equipment/{id}/ai-assessment` is currently a mock implementation returning deterministic structured data.
