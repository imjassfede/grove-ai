import operator
from typing import Annotated, Any, TypedDict


class RootCause(TypedDict):
    cause: str
    evidence: str
    impact: str


class Insight(TypedDict):
    insight: str
    confidence: float
    agents: list[str]
    category: str


class Recommendation(TypedDict):
    action: str
    priority: str
    effort: str
    impact: str
    timeline: str
    owner: str


class Experiment(TypedDict):
    hypothesis: str
    impact_score: float
    confidence_score: float
    ease_score: float
    ice_score: float
    measurement: str
    timeline: str


class GrowthState(TypedDict):
    # Input
    challenge: str
    analysis_id: str
    domain: str

    # Classification
    business_area: str
    problem_type: str
    urgency: str
    key_questions: list[str]

    # Planning
    selected_agents: list[str]
    agent_focus: dict[str, list[str]]

    # Agent results — merged via dict union as agents run in parallel
    agent_results: Annotated[dict[str, Any], operator.or_]
    agent_trace: dict[str, Any]

    # Synthesis
    root_causes: list[RootCause]
    insights: list[Insight]
    recommendations: list[Recommendation]
    experiments: list[Experiment]
    executive_summary: str

    # Progress tracking
    status: str
    progress: Annotated[list[str], operator.add]
    error: str | None
