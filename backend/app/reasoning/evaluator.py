import json

from google import genai
from google.genai import types

from app.config.settings import get_settings
from app.reasoning.state import GrowthState

_client = genai.Client(api_key=get_settings().google_api_key)
_MODEL = "gemini-3.6-flash"

_SYSTEM = """You are Grove's senior strategy synthesizer. Produce an evidence-backed Growth Intelligence Report from specialist research, critic findings, and the evidence graph. Never invent facts. Separate facts, inferences, and hypotheses. Recommendations must be traceable to evidence."""

_PROMPT = """Business challenge: {challenge}
Company domain: {domain}

SPECIALIST INTELLIGENCE:
{agent_results}

CRITIC:
{critic}

EVIDENCE GRAPH:
{graph}

PRIOR ANALYSIS MEMORY:
{memory}

Return JSON only:
{{
  "executive_summary": "<2-3 sentence summary>",
  "root_causes": [{{"cause":"...","evidence":"...","impact":"high|medium|low"}}],
  "insights": [{{"insight":"...","confidence":0.0,"agents":["..."],"category":"market|customer|competitive|revenue|product|gtm"}}],
  "recommendations": [{{"action":"...","priority":"p1|p2|p3","effort":"low|medium|high","impact":"low|medium|high","timeline":"...","owner":"..."}}],
  "experiments": [{{"hypothesis":"If X, expect Y because Z","impact_score":1,"confidence_score":1,"ease_score":1,"ice_score":1,"measurement":"...","timeline":"..."}}]
}}

Rules: 3-5 root causes; 4-6 insights; 3-6 recommendations; 2-4 experiments. Every root cause and recommendation must be traceable to grounded evidence. If evidence is weak or contradictory, explicitly reflect lower confidence or a data gap."""


async def evaluate(state: GrowthState) -> dict:
    agent_results = state.get("agent_results", {})
    trace_summary = {
        name: {
            "iterations": len(result.get("agent_trace", [])),
            "findings": len(result.get("findings", [])),
            "sources": len(result.get("grounding_sources", [])),
            "queries": result.get("search_queries", []),
        }
        for name, result in agent_results.items()
    }
    user_message = _PROMPT.format(
        challenge=state["challenge"],
        domain=state.get("domain", ""),
        agent_results=json.dumps(agent_results, indent=2)[-50000:],
        critic=json.dumps(state.get("critic", {}), indent=2),
        graph=json.dumps(state.get("knowledge_graph", {}), indent=2)[-20000:],
        memory=json.dumps(state.get("research_memory", []), indent=2),
    )
    tools = [{"code_execution": {}}]
    if state.get("domain"):
        tools.extend([{"url_context": {}}, {"google_search": {}}])
    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=user_message,
        config=types.GenerateContentConfig(system_instruction=_SYSTEM, response_mime_type="application/json", tools=tools),
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
        "agent_trace": trace_summary,
        "critic": state.get("critic", {}),
        "knowledge_graph": state.get("knowledge_graph", {}),
        "status": "complete",
        "progress": ["Analysis complete — multi-agent evidence, critic, memory, and synthesis ready"],
    }
    if synthesis_sources:
        result["agent_results"] = {"synthesis": {"grounding_sources": synthesis_sources}}
    return result
