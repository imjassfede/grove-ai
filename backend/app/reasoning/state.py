import operator
from typing import Annotated, Any, TypedDict


class RootCause(TypedDict):
    cause: str
    evidence: str
    impact: str  # "high" | "medium" | "low"


class Insight(TypedDict):
    insight: str
    confidence: float
    agents: list[str]
    category: str


class Recommendation(TypedDict):
    action: str
    priority: str   # "p1" | "p2" | "p3"
    effort: str     # "low" | "medium" | "high"
    impact: str     # "low" | "medium" | "high"
    timeline: str
    owner: str


class Experiment(TypedDict):
    hypothesis: str
    impact_score: float   # 1-10
    confidence_score: float
    ease_score: float
    ice_score: float      # composite
    measurement: str
    timeline: str


class GrowthState(TypedDict):
    # Input
    challenge: str
    analysis_id: str

    # Classification (set by classifier node)
    business_area: str
    problem_type: str
    urgency: str           # "critical" | "high" | "medium" | "low"
    key_questions: list[str]

    # Planning (set by planner node)
    selected_agents: list[str]
    agent_focus: dict[str, list[str]]  # agent_name → focus areas

    # Agent results — merged via dict union as agents run in parallel
    agent_results: Annotated[dict[str, Any], operator.or_]

    # Synthesis (set by evaluator node)
    root_causes: list[RootCause]
    insights: list[Insight]
    recommendations: list[Recommendation]
    experiments: list[Experiment]
    executive_summary: str

    # Progress tracking
    status: str            # classifying | planning | analyzing | synthesizing | complete | error
    progress: Annotated[list[str], operator.add]
    error: str | None
