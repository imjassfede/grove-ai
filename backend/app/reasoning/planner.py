from app.config.llm import complete
from app.reasoning.state import GrowthState

_AVAILABLE_AGENTS = {
    "market": "Analyzes market dynamics, trends, TAM/SAM/SOM, and market opportunities",
    "customer": "Investigates customer pain points, personas, behavior, and voice-of-customer signals",
    "competitor": "Benchmarks competitors on positioning, pricing, features, and market gaps",
    "revenue": "Diagnoses revenue performance, funnel metrics, conversion rates, and growth levers",
    "experiment": "Designs growth experiments with ICE scoring, hypotheses, and measurement plans",
    "gtm": "Develops go-to-market strategy including ICP, positioning, channels, and messaging",
}

_SYSTEM = """You are a growth strategy orchestrator. Given a classified business problem,
you select the minimal set of intelligence agents needed to produce the best diagnosis.
Less is more — only include agents that are directly relevant.

You MUST respond with valid JSON only."""

_PROMPT = """Business challenge: "{challenge}"

Classification:
- Area: {business_area}
- Type: {problem_type}
- Urgency: {urgency}
- Key questions: {key_questions}

Available agents:
{agents_list}

Select the 2-4 most relevant agents and define specific focus areas for each.

Return JSON:
{{
  "selected_agents": ["<agent_name>", ...],
  "agent_focus": {{
    "<agent_name>": ["<specific focus 1>", "<specific focus 2>", "<specific focus 3>"]
  }},
  "reasoning": "<brief explanation of agent selection>"
}}"""


async def plan(state: GrowthState) -> dict:
    agents_list = "\n".join(f"- {name}: {desc}" for name, desc in _AVAILABLE_AGENTS.items())

    data = await complete(
        _SYSTEM,
        _PROMPT.format(
            challenge=state["challenge"],
            business_area=state["business_area"],
            problem_type=state["problem_type"],
            urgency=state["urgency"],
            key_questions="\n".join(f"  - {q}" for q in state["key_questions"]),
            agents_list=agents_list,
        ),
    )

    selected = data["selected_agents"]
    return {
        "selected_agents": selected,
        "agent_focus": data["agent_focus"],
        "status": "analyzing",
        "progress": [f"Dispatching {len(selected)} agents: {', '.join(selected)}"],
    }
