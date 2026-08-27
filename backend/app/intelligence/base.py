import json
from abc import ABC, abstractmethod

from google import genai
from google.genai import types

from app.config.settings import get_settings
from app.intelligence.specs import AGENT_SPECS

_client = genai.Client(api_key=get_settings().google_api_key)
_MODEL = "gemini-3.6-flash"


class BaseIntelligenceAgent(ABC):
    name: str
    description: str
    system_prompt: str

    def _get_spec(self):
        return AGENT_SPECS[self.name]

    def _build_research_prompt(self, state: dict, iteration: int, previous: str) -> str:
        challenge = state["challenge"]
        domain = state.get("domain", "").strip()
        focus_areas = state.get("focus_areas") or state.get("agent_focus", {}).get(self.name, [])
        key_questions = state.get("key_questions", [])
        shared_results = state.get("agent_results", {})
        prior_memory = state.get("research_memory", [])
        critic = state.get("critic", {})
        followup_focus = state.get("followup_focus", "")
        spec = self._get_spec()
        company_url = domain if domain.startswith("http") else (f"https://{domain}" if domain else "")
        focus_text = "\n".join(f"- {f}" for f in focus_areas) if focus_areas else "General analysis"
        questions_text = "\n".join(f"- {q}" for q in key_questions) if key_questions else "- Determine the most decision-critical unknowns."
        tasks_text = "\n".join(f"- {task}" for task in spec.research_tasks)
        sources_text = ", ".join(spec.preferred_sources)
        tools_text = ", ".join(spec.tools)
        previous_text = previous[-8000:] if previous else "No previous iteration. Start by forming a research plan and gathering evidence."
        shared_text = json.dumps(shared_results, indent=2) if shared_results else "No upstream specialist results are available yet."
        if len(shared_text) > 22000:
            shared_text = shared_text[-22000:]
        memory_text = json.dumps(prior_memory[-2:], indent=2) if prior_memory else "No prior completed analyses are available."
        critic_text = json.dumps(critic, indent=2)[-10000:] if critic else "No cross-agent critic feedback yet."

        company_rules = (
            "Start from the official site, then corroborate important claims with independent sources. Use live web research whenever a claim depends on current public information."
            if company_url else
            "No company domain was supplied. Do not invent company-specific facts; explicitly label assumptions and data gaps."
        )
        quantitative_rule = (
            "When doing arithmetic, unit economics, percentages, ICE scores, or statistical calculations, use code_execution rather than mental arithmetic."
            if "code_execution" in spec.tools else ""
        )
        followup_rule = (
            f"This is a targeted follow-up. Prioritize closing this critic-identified gap: {followup_focus}. Do not repeat the previous research unless verification is necessary."
            if followup_focus else ""
        )

        return f"""You are running iteration {iteration} of a bounded agentic research loop.

Business challenge: "{challenge}"
Company domain: {domain or "not provided"}
Official company URL: {company_url or "not provided"}

Your objective:
{spec.objective}

Your specialist research tasks:
{tasks_text}

Current focus areas:
{focus_text}

Diagnostic questions:
{questions_text}

Preferred evidence sources:
{sources_text}
Tools enabled: {tools_text}

{company_rules}
{quantitative_rule}
{followup_rule}

Shared intelligence from upstream specialists:
{shared_text}

Cross-agent critic feedback:
{critic_text}

Relevant memory from prior completed analyses:
{memory_text}

Previous iteration output from this specialist:
{previous_text}

Agentic loop rules:
1. Inspect upstream intelligence and critic feedback before deciding what to research.
2. Research only the highest-value missing evidence.
3. Prefer primary, recent, independent sources and corroborate material claims.
4. Distinguish observed facts from inferences and hypotheses.
5. Never invent metrics, competitors, pricing, customers, or market share.
6. Challenge weak conclusions and search for contradictory evidence when useful.
7. If an upstream claim materially changes your analysis, verify it when possible.
8. Stop when evidence is sufficient; do not research for its own sake.

Return JSON only:
{{
  "competitors": [
    {{"name": "<name>", "rank": <1-3>, "relevance": "<why this is a top competitor>", "evidence": "<supporting evidence>", "source_urls": ["<url>"]}}
  ],
  "findings": [
    {{"finding": "<specific finding>", "significance": "<high|medium|low>", "evidence": "<observed evidence and why it matters>", "evidence_type": "<observed|inferred>", "source_urls": ["<url>"]}}
  ],
  "insights": [
    {{"insight": "<actionable insight>", "confidence": <0.0-1.0>, "source_urls": ["<url>"]}}
  ],
  "risks": ["<risk>"],
  "opportunities": ["<opportunity>"],
  "data_gaps": ["<specific missing evidence>"],
  "search_queries": ["<important query actually used>"],
  "research_status": "<continue|sufficient>"
}}

Quality bar:
- At least {spec.min_findings} substantive findings and 2 insights.
- Competitor agent should return exactly 3 validated competitors when evidence permits.
- Every important finding should have a source when public evidence exists.
- Generic advice is not a finding.
"""

    async def run(self, state: dict) -> dict:
        spec = self._get_spec()
        previous = ""
        final_result: dict | None = None
        all_sources: dict[str, dict[str, str]] = {}
        iteration_log: list[dict[str, object]] = []

        for iteration in range(1, spec.max_iterations + 1):
            response = await _client.aio.models.generate_content(
                model=_MODEL,
                contents=self._build_research_prompt(state, iteration, previous),
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    max_output_tokens=3500,
                    tools=([{"url_context": {}}] if "url_context" in spec.tools and state.get("domain", "").strip() else [])
                    + ([{"google_search": {}}] if "web_search" in spec.tools else [])
                    + ([{"code_execution": {}}] if "code_execution" in spec.tools else [])
                    or None,
                ),
            )
            result = json.loads(response.text)
            result["agent"] = self.name
            result["iteration"] = iteration
            sources = []
            try:
                metadata = response.candidates[0].grounding_metadata
                for chunk in metadata.grounding_chunks or []:
                    if chunk.web and chunk.web.uri:
                        source = {"title": chunk.web.title or "Web source", "url": chunk.web.uri}
                        all_sources[source["url"]] = source
                        sources.append(source)
            except (AttributeError, IndexError, TypeError):
                pass
            iteration_log.append({"iteration": iteration, "status": result.get("research_status", "continue"), "findings": len(result.get("findings", [])), "sources": len(sources), "search_queries": result.get("search_queries", [])})
            previous = response.text
            final_result = result
            if result.get("research_status") == "sufficient" and len(result.get("findings", [])) >= spec.min_findings:
                break

        assert final_result is not None
        if all_sources:
            final_result["grounding_sources"] = list(all_sources.values())
        final_result["agent_trace"] = iteration_log
        return {
            "agent_results": {self.name: final_result},
            "progress": [f"{self.name} intelligence complete — {len(final_result.get('findings', []))} findings, {len(iteration_log)} research iteration(s), {len(all_sources)} web sources"],
        }

    @abstractmethod
    def _get_system_prompt(self) -> str: ...
