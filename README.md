# Mini Healthcare Equipment API

Async FastAPI backend for managing hospital departments, equipment inventory, and equipment requests.

## Tech Stack
- FastAPI
- SQLAlchemy 2.x (Async)
- Alembic
- PostgreSQL (`asyncpg`) or SQLite (`aiosqlite`)
- Pydantic v2
- Pytest + HTTPX (tests)

## Project Structure
```text
.
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── response.py
│   │   └── v1/
│   │       ├── departments.py
│   │       ├── equipment.py
│   │       └── equipment_requests.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── repositories/         # ORM models
│   │   ├── department.py
│   │   ├── equipment.py
│   │   ├── equipment_request.py
│   │   └── enums.py
│   ├── schemas/
│   │   ├── department.py
│   │   ├── equipment.py
│   │   ├── equipment_request.py
│   │   └── ai.py
│   └── services/
│       ├── department_service.py
│       ├── equipment_service.py
│       ├── equipment_request_service.py
│       └── ai_assessment_service.py
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   └── test_equipment_request_rules.py
├── llm_design.md
├── pyproject.toml
└── requirements.txt
```

## Setup (Poetry)
```bash
poetry install --with dev
cp .env.example .env
```

Update `.env` with your DB settings.

## Setup (pip)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## DB Migration
```bash
alembic upgrade head
```

## Run Server
```bash
poetry run uvicorn app.main:app --reload
```

Open docs: `http://127.0.0.1:8000/docs`

## API Endpoints
- `POST /departments`
- `GET /departments?organization_id=1`
- `POST /equipment`
- `GET /equipment/{id}`
- `GET /equipment?department_id=1&status=available&page=1&page_size=20`
- `PUT /equipment/{id}`
- `POST /equipment-requests`
- `PATCH /equipment-requests/{id}/approve`
- `GET /equipment-requests?organization_id=1&page=1&page_size=20`
- `POST /equipment/{id}/ai-assessment` (mock AI)

## Response Format
Success:
```json
{
  "success": true,
  "message": "Equipment created successfully",
  "data": {}
}
```

Error:
```json
{
  "success": false,
  "message": "Equipment not found",
  "errors": {}
}
```

## Tests
```bash
poetry run pytest
```

## Notes
- `llm_design.md` explains how to replace the mock AI endpoint with a real Anthropic/OpenAI integration (prompting, parsing, retries, fallback, cache).
