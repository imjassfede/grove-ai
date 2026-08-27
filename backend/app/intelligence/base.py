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
        focus_areas = state.get("focus_areas", [])
        key_questions = state.get("key_questions", [])
        spec = self._get_spec()
        company_url = domain if domain.startswith("http") else (f"https://{domain}" if domain else "")

        focus_text = "\n".join(f"- {f}" for f in focus_areas) if focus_areas else "General analysis"
        questions_text = "\n".join(f"- {q}" for q in key_questions) if key_questions else "- Determine the most decision-critical unknowns."
        tasks_text = "\n".join(f"- {task}" for task in spec.research_tasks)
        sources_text = ", ".join(spec.preferred_sources)
        tools_text = ", ".join(spec.tools)
        previous_text = previous[-12000:] if previous else "No previous iteration. Start by forming a research plan and gathering evidence."

        company_rules = (
            "The company domain is available. Start from the official site, then corroborate important claims with independent sources. "
            "Use live web research whenever a claim depends on current public information."
            if company_url
            else "No company domain was supplied. Do not invent company-specific facts; explicitly label assumptions and data gaps."
        )

        quantitative_rule = (
            "When doing arithmetic, unit economics, percentages, ICE scores, or statistical calculations, use the code_execution tool rather than mental arithmetic."
            if "code_execution" in spec.tools else ""
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

Tools enabled for this specialist:
{tools_text}

{company_rules}
{quantitative_rule}

Previous iteration output:
{previous_text}

Agentic loop rules:
1. Decide what evidence is still missing before concluding.
2. Use the enabled tools to research the highest-value unknowns.
3. Prefer primary, recent, and independent sources; corroborate material claims.
4. Distinguish observed facts from inferences and hypotheses.
5. Never invent pricing, revenue, market share, customer counts, conversion rates, or other metrics.
6. On later iterations, challenge weak conclusions and search for contradictory evidence.
7. Stop when the evidence is sufficient for the objective; do not research for its own sake.

Return JSON only:
{{
  "findings": [
    {{
      "finding": "<specific finding>",
      "significance": "<high|medium|low>",
      "evidence": "<observed evidence and why it matters>",
      "evidence_type": "<observed|inferred>",
      "source_urls": ["<source URL>"]
    }}
  ],
  "insights": [
    {{"insight": "<actionable insight>", "confidence": <0.0-1.0>, "source_urls": ["<source URL>"]}}
  ],
  "risks": ["<risk>"],
  "opportunities": ["<opportunity>"],
  "data_gaps": ["<specific missing evidence>"],
  "search_queries": ["<important query actually used>"],
  "research_status": "<continue|sufficient>"
}}

Quality bar:
- At least {spec.min_findings} substantive findings and 2 insights.
- Every important finding should have a source when public evidence exists.
- Generic advice is not a finding.
- If evidence is weak, say so explicitly.
"""

    async def run(self, state: dict) -> dict:
        spec = self._get_spec()
        previous = ""
        final_result: dict | None = None
        all_sources: dict[str, dict[str, str]] = {}
        iteration_log: list[dict[str, object]] = []

        for iteration in range(1, spec.max_iterations + 1):
            user_message = self._build_research_prompt(state, iteration, previous)
            tools = []
            if "url_context" in spec.tools and state.get("domain", "").strip():
                tools.append({"url_context": {}})
            if "web_search" in spec.tools:
                tools.append({"google_search": {}})
            if "code_execution" in spec.tools:
                tools.append({"code_execution": {}})

            response = await _client.aio.models.generate_content(
                model=_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    response_mime_type="application/json",
                    tools=tools or None,
                ),
            )
            result = json.loads(response.text)
            result["agent"] = self.name
            result["iteration"] = iteration

            sources: list[dict[str, str]] = []
            try:
                metadata = response.candidates[0].grounding_metadata
                for chunk in metadata.grounding_chunks or []:
                    if chunk.web and chunk.web.uri:
                        source = {"title": chunk.web.title or "Web source", "url": chunk.web.uri}
                        all_sources[source["url"]] = source
                        sources.append(source)
            except (AttributeError, IndexError, TypeError):
                pass

            iteration_log.append({
                "iteration": iteration,
                "status": result.get("research_status", "continue"),
                "findings": len(result.get("findings", [])),
                "sources": len(sources),
                "search_queries": result.get("search_queries", []),
            })
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
            "progress": [
                f"{self.name} intelligence complete — {len(final_result.get('findings', []))} findings, "
                f"{len(iteration_log)} research iteration(s), {len(all_sources)} web sources"
            ],
        }

    @abstractmethod
    def _get_system_prompt(self) -> str: ...
