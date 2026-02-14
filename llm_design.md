# LLM Integration Design (Simple and Practical)

## 1) What we have now (Mock)
- Endpoint: `POST /equipment/{id}/ai-assessment`
- It **does not call any external AI provider**.
- It returns simulated JSON:
  - `risk_score` (1-10)
  - `risk_factors` (list)
  - `recommendations` (list)

---

## 2) How to replace mock with real LLM later

### Step A: Create an AI provider service
- File example: `app/services/llm_provider_service.py`
- Responsibility: only call Anthropic/OpenAI and return text.
- Keep route/service logic separate from provider SDK code.

### Step B: Prompt structure
Use two parts:

1. **System instruction**
- \"You are a healthcare equipment security analyst.\"
- \"Return strict JSON only with keys: risk_score, risk_factors, recommendations.\"
- \"risk_score must be integer from 1 to 10.\"

2. **User input**
- Equipment info: `name`, `manufacturer`, `model_number`, `category`, `status`
- Operational input: `environment`, `usage_pattern`, `known_issues`, `internet_connected`, `last_maintenance_days`

This keeps prompt deterministic and easy to parse.

### Step C: Parse and validate response
- LLM returns text.
- Parse JSON safely.
- Validate using `AIAssessmentOutput` Pydantic schema.
- If invalid JSON or invalid shape: treat as provider error/fallback.

---

## 3) Failure handling strategy

### Retry
- Retry 2-3 times with exponential backoff.
- Example delays: 0.5s, 1s, 2s.

### Fallback
- If all retries fail:
  - Option 1: return last cached valid assessment.
  - Option 2: return safe default assessment with higher risk note.

### Observability
- Log provider latency, failures, and retry counts.
- Add request id in logs for traceability.

---

## 4) Caching strategy

### Why
- Same equipment + same input should not call LLM repeatedly.
- Reduces latency and cost.

### Cache key
- `equipment_id`
- `equipment.updated_at`
- hash of assessment input payload

Example:
`ai_assessment:{equipment_id}:{updated_at}:{payload_hash}`

### TTL
- Suggested TTL: 24 hours (adjust per business need).

---

## 5) Security and compliance notes
- Do not send sensitive PHI unless necessary.
- Keep provider API key in environment variables only.
- Store minimal request/response logs (no secrets).

---

## 6) Current state summary
- The mock AI assessment endpoint is implemented with a clean extension point for future LLM integration.
- The architecture allows replacing the mock logic with a real provider without changing the API contract or business layer.
