import json

from app.config.llm import complete
from app.reasoning.state import GrowthState

_SYSTEM = """You are a senior management consultant synthesizing intelligence from multiple business analysts.
Your job is to combine their findings into a clear, structured, and actionable Growth Intelligence Report.

You MUST respond with valid JSON only."""

_PROMPT = """Business challenge: "{challenge}"

Agent findings:
{agent_results}

Synthesize all findings into a comprehensive growth intelligence report.

Return JSON with this structure:
{{
  "executive_summary": "<2-3 sentence summary of the situation and recommended path forward>",
  "root_causes": [
    {{
      "cause": "<root cause>",
      "evidence": "<supporting evidence from agent findings>",
      "impact": "<high|medium|low>"
    }}
  ],
  "insights": [
    {{
      "insight": "<key insight>",
      "confidence": <0.0-1.0>,
      "agents": ["<agent names that support this>"],
      "category": "<market|customer|competitive|revenue|product|gtm>"
    }}
  ],
  "recommendations": [
    {{
      "action": "<specific, actionable recommendation>",
      "priority": "<p1|p2|p3>",
      "effort": "<low|medium|high>",
      "impact": "<low|medium|high>",
      "timeline": "<e.g. 2 weeks, 1 month, Q2>",
      "owner": "<e.g. Marketing, Product, Sales, CEO>"
    }}
  ],
  "experiments": [
    {{
      "hypothesis": "<If we do X, we expect Y because Z>",
      "impact_score": <1-10>,
      "confidence_score": <1-10>,
      "ease_score": <1-10>,
      "ice_score": <composite 1-10>,
      "measurement": "<how to measure success>",
      "timeline": "<experiment duration>"
    }}
  ]
}}

Rules:
- root_causes: 3-5 causes, ordered by impact
- insights: 4-6 insights, most confident first
- recommendations: 3-6 actions, p1 first
- experiments: 2-4 experiments, highest ICE score first
- Be specific and actionable — no generic advice"""


async def evaluate(state: GrowthState) -> dict:
    agent_results_text = ""
    for agent_name, result in state.get("agent_results", {}).items():
        agent_results_text += f"\n\n=== {agent_name.upper()} INTELLIGENCE ===\n"
        agent_results_text += json.dumps(result, indent=2)

    data = await complete(
        _SYSTEM,
        _PROMPT.format(
            challenge=state["challenge"],
            agent_results=agent_results_text,
        ),
    )

    return {
        "executive_summary": data["executive_summary"],
        "root_causes": data["root_causes"],
        "insights": data["insights"],
        "recommendations": data["recommendations"],
        "experiments": data["experiments"],
        "status": "complete",
        "progress": ["Analysis complete — Growth Intelligence Report ready"],
    }
