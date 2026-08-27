from app.config.llm import complete
from app.intelligence.specs import AGENT_SPECS
from app.reasoning.state import GrowthState

_SYSTEM = """You are Grove's research workflow planner.

Grove is a collaborative intelligence system, not a collection of independent chatbots.
The workflow has a fixed first research phase and a fixed synthesis phase:
1. competitor discovers and validates the top 3 competitors;
2. market, customer, revenue, and gtm investigate in parallel using that competitor dossier;
3. experiment turns the combined evidence into testable priorities;
4. evaluator synthesizes the final report.

Your job is to define the concrete focus areas for each specialist. Preserve the collaboration pattern: downstream specialists must build on the competitive dossier rather than ignoring it.

You MUST respond with valid JSON only."""

_PROMPT = """Business challenge: "{challenge}"

Classification:
- Area: {business_area}
- Type: {problem_type}
- Urgency: {urgency}
- Key questions: {key_questions}

Available specialist capabilities:
{agents_list}

Define 2-4 concrete focus areas for EACH of these research specialists:
- competitor: must discover and validate the top 3 competitors and create the shared competitive dossier.
- market: must use the competitor dossier and include market, customer, macro, regulatory, technology, and geopolitical analysis where relevant.
- customer: must use the competitor dossier to compare customer segments, voice of customer, needs, objections, and unmet needs.
- revenue: must use the competitor dossier to compare pricing, packaging, monetization, and commercial models.
- gtm: must use the competitor dossier to compare ICP, positioning, channels, sales motion, partnerships, and geographic focus.
- experiment: must use all upstream intelligence to identify the highest-leverage uncertainties and experiments.

Do not make the specialists independent. Explicitly state the cross-agent question each specialist should answer.

Return JSON:
{{
  "selected_agents": ["competitor", "market", "customer", "revenue", "gtm", "experiment"],
  "agent_focus": {{
    "competitor": ["<specific focus>", "<specific focus>"],
    "market": ["<specific focus>", "<specific focus>"],
    "customer": ["<specific focus>", "<specific focus>"],
    "revenue": ["<specific focus>", "<specific focus>"],
    "gtm": ["<specific focus>", "<specific focus>"],
    "experiment": ["<specific focus>", "<specific focus>"]
  }},
  "reasoning": "<brief explanation of the research sequence>"
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

    workflow_agents = ["competitor", "market", "customer", "revenue", "gtm", "experiment"]
    focus = data.get("agent_focus", {})

    return {
        "selected_agents": workflow_agents,
        "agent_focus": {name: focus.get(name, []) for name in workflow_agents},
        "status": "analyzing",
        "progress": [
            "Planned collaborative research pipeline: competitor discovery → cross-specialist research → experiments → synthesis"
        ],
    }
