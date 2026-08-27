import json

from google import genai
from google.genai import types

from app.config.settings import get_settings
from app.reasoning.state import GrowthState

_client = genai.Client(api_key=get_settings().google_api_key)
_MODEL = "gemini-2.5-flash"

_SYSTEM = """You are a senior management consultant synthesizing grounded intelligence from multiple business analysts.
Your job is to combine evidence into a clear, structured, and actionable Growth Intelligence Report.

Evidence discipline is mandatory:
- Prefer observed facts supported by web sources over model assumptions.
- Never turn an inference into a fact.
- Do not invent company metrics, customer counts, pricing, market share, competitors, or performance data.
- If evidence conflicts or is weak, lower confidence and state the data gap.
- Recommendations must follow from the strongest evidence, not generic growth advice.

You MUST respond with valid JSON only."""

_PROMPT = """Business challenge: "{challenge}"
Company domain: "{domain}"

Agent findings:
{agent_results}

Synthesize all findings into a comprehensive growth intelligence report.

Return JSON with this structure:
{{
  "executive_summary": "<2-3 sentence summary of the situation and recommended path forward>",
  "root_causes": [
    {{
      "cause": "<root cause>",
      "evidence": "<specific supporting evidence from the grounded findings>",
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
      "action": "<specific, actionable recommendation tied to evidence>",
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
- Every root cause and recommendation must be traceable to at least one grounded agent finding.
- Be specific and actionable — no generic advice."""


async def evaluate(state: GrowthState) -> dict:
    agent_results_text = ""
    for agent_name, result in state.get("agent_results", {}).items():
        agent_results_text += f"\n\n=== {agent_name.upper()} INTELLIGENCE ===\n"
        agent_results_text += json.dumps(result, indent=2)

    user_message = _PROMPT.format(
        challenge=state["challenge"],
        domain=state.get("domain", ""),
        agent_results=agent_results_text,
    )

    tools = [{"google_search": {}}] if state.get("domain") else None
    if state.get("domain"):
        user_message += "\n\nUse live web search to verify the most decision-critical company-specific claims before finalizing the report."

    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM,
            response_mime_type="application/json",
            tools=tools,
        ),
    )
    data = json.loads(response.text)

    synthesis_sources: list[dict[str, str]] = []
    try:
        metadata = response.candidates[0].grounding_metadata
        for chunk in metadata.grounding_chunks or []:
            if chunk.web and chunk.web.uri:
                synthesis_sources.append({"title": chunk.web.title or "Web source", "url": chunk.web.uri})
    except (AttributeError, IndexError, TypeError):
        pass

    result = {
        "executive_summary": data["executive_summary"],
        "root_causes": data["root_causes"],
        "insights": data["insights"],
        "recommendations": data["recommendations"],
        "experiments": data["experiments"],
        "status": "complete",
        "progress": [
            "Analysis complete — grounded Growth Intelligence Report ready"
            + (f" · {len(synthesis_sources)} verification sources" if synthesis_sources else "")
        ],
    }
    if synthesis_sources:
        result["agent_results"] = {"synthesis": {"grounding_sources": synthesis_sources}}
    return result
