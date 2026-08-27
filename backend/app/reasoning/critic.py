import json
from urllib.parse import urlparse

from google import genai
from google.genai import types

from app.config.settings import get_settings
from app.intelligence.specs import AGENT_SPECS
from app.knowledge.graph import build_knowledge_graph
from app.reasoning.state import GrowthState

_client = genai.Client(api_key=get_settings().google_api_key)
_MODEL = "gemini-3.6-flash"
# One critic + at most one targeted follow-up is enough to preserve the
# agentic correction loop without turning every analysis into a long chain.
_MAX_ROUNDS = 1

_SYSTEM = """You are Grove's cross-agent research critic.
You inspect shared intelligence, evidence quality, contradictions, and unresolved questions. Decide whether one targeted specialist follow-up can materially improve the analysis. Never invent facts. Return valid JSON only."""


def _source_score(url: str) -> float:
    host = urlparse(url or "").netloc.lower()
    if not host:
        return 0.0
    score = 0.55
    if host.endswith((".gov", ".gov.uk", ".eu", ".int")):
        score += 0.25
    if any(x in host for x in ("sec.gov", "who.int", "worldbank.org", "oecd.org", "imf.org")):
        score += 0.15
    if any(x in host for x in ("reuters.com", "ft.com", "economist.com")):
        score += 0.10
    return min(score, 1.0)


def _score_sources(results: dict) -> list[dict]:
    scored = []
    for agent, result in results.items():
        for source in result.get("grounding_sources", []):
            url = source.get("url", "")
            scored.append({"agent": agent, "url": url, "title": source.get("title", "Web source"), "quality": round(_source_score(url), 2)})
    return sorted(scored, key=lambda x: x["quality"], reverse=True)


async def critique(state: GrowthState) -> dict:
    results = state.get("agent_results", {})
    compact = json.dumps(results, indent=2)
    if len(compact) > 45000:
        compact = compact[-45000:]
    source_scores = _score_sources(results)
    graph = build_knowledge_graph(results)

    prompt = f"""Business challenge: {state['challenge']}
Company domain: {state.get('domain', '')}
Research round: {state.get('research_round', 0)} of {_MAX_ROUNDS}

Shared specialist intelligence:
{compact}

Knowledge graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} evidence relations.
Source quality signals:
{json.dumps(source_scores[:40], indent=2)}

Available specialists: {', '.join(AGENT_SPECS)}

Check:
- unsupported, stale, duplicated, or single-source claims
- contradictions between specialists
- assumptions presented as facts
- the highest-value unanswered question
- which ONE specialist should perform a targeted follow-up, if any

Return:
{{
  "decision": "<continue_research|sufficient>",
  "followup_agent": "<one agent name or null>",
  "reason": "<why>",
  "contradictions": [{{"claim_a": "...", "claim_b": "...", "agents": ["..."], "severity": "high|medium|low"}}],
  "weak_claims": ["..."],
  "missing_evidence": ["..."],
  "source_quality": "<high|medium|low>"
}}
"""
    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=_SYSTEM, response_mime_type="application/json"),
    )
    data = json.loads(response.text)
    followup = data.get("followup_agent")
    round_no = state.get("research_round", 0)
    if round_no >= _MAX_ROUNDS or data.get("decision") == "sufficient":
        data["decision"] = "sufficient"
        followup = None
    if followup not in AGENT_SPECS:
        followup = None
    data["source_scores"] = source_scores[:40]
    data["knowledge_graph"] = {"node_count": len(graph["nodes"]), "edge_count": len(graph["edges"])}
    data.setdefault("contradictions", [])
    return {
        "critic": data,
        "followup_agent": followup,
        "research_round": round_no + 1,
        "knowledge_graph": graph,
        "progress": ["Cross-agent critic completed — " + (f"targeted follow-up: {followup}" if followup else "evidence sufficient")],
    }
