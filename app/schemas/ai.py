from pydantic import BaseModel, Field


class AIAssessmentInput(BaseModel):
    environment: str = Field(min_length=2, max_length=120)
    usage_pattern: str = Field(min_length=2, max_length=250)
    known_issues: list[str] = Field(default_factory=list)
    internet_connected: bool = False
    last_maintenance_days: int | None = Field(default=None, ge=0)


class AIAssessmentOutput(BaseModel):
    risk_score: int = Field(ge=1, le=10)
    risk_factors: list[str]
    recommendations: list[str]
