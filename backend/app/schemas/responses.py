import uuid
from datetime import datetime

from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    id: uuid.UUID
    challenge: str
    status: str
    business_area: str | None = None
    problem_type: str | None = None
    urgency: str | None = None
    selected_agents: list[str] | None = None
    agent_results: dict | None = None
    root_causes: list | None = None
    insights: list | None = None
    recommendations: list | None = None
    experiments: list | None = None
    executive_summary: str | None = None
    progress: list[str] | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AnalysisListResponse(BaseModel):
    analyses: list[AnalysisResponse]
    total: int
