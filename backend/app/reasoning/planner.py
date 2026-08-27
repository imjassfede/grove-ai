from app.config.llm import complete
from app.intelligence.specs import AGENT_SPECS
from app.reasoning.state import GrowthState

_SYSTEM = """You are a growth strategy orchestrator. Given a classified business problem,
you select the minimal set of specialist agents needed to produce the best diagnosis.
Agents have different research capabilities; dispatch based on the work required, not just topic similarity.
Less is more — only include agents that are directly relevant.

You MUST respond with valid JSON only."""

_PROMPT = """Business challenge: "{challenge}"

Classification:
- Area: {business_area}
- Type: {problem_type}
- Urgency: {urgency}
- Key questions: {key_questions}

Available specialist agents and capabilities:
{agents_list}

Select 2-4 relevant agents. For each, define 2-4 concrete focus areas that can be investigated with its available capabilities.
Do not assign a specialist work that belongs to another agent unless necessary.

Return JSON:
{{
  "selected_agents": ["<agent_name>", ...],
  "agent_focus": {{
    "<agent_name>": ["<specific research focus 1>", "<specific research focus 2>"]
  }},
  "reasoning": "<brief explanation of agent selection>"
}}"""


def _capabilities_text() -> str:
    blocks = []
    for name, spec in AGENT_SPECS.items():
        blocks.append(
            f"- {name}: {spec.objective}\n"
            f"  Research: {'; '.join(spec.research_tasks)}\n"
            f"  Tools: {', '.join(spec.tools)}\n"
            f"  Preferred evidence: {', '.join(spec.preferred_sources)}"
        )
    return "\n".join(blocks)


async def plan(state: GrowthState) -> dict:
    data = await complete(
        _SYSTEM,
        _PROMPT.format(
            challenge=state["challenge"],
            business_area=state["business_area"],
            problem_type=state["problem_type"],
            urgency=state["urgency"],
            key_questions="\n".join(f"  - {q}" for q in state["key_questions"]),
            agents_list=_capabilities_text(),
        ),
    )

    selected = [name for name in data["selected_agents"] if name in AGENT_SPECS][:4]
    if len(selected) < 2:
        selected = list(AGENT_SPECS)[:2]

    return {
        "selected_agents": selected,
        "agent_focus": {name: data["agent_focus"].get(name, []) for name in selected},
        "status": "analyzing",
        "progress": [f"Dispatching {len(selected)} capability-aware agents: {', '.join(selected)}"],
    }
