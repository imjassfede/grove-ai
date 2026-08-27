import json
from abc import ABC, abstractmethod

from google import genai
from google.genai import types

from app.config.settings import get_settings

_client = genai.Client(api_key=get_settings().google_api_key)
_MODEL = "gemini-2.5-flash"


class BaseIntelligenceAgent(ABC):
    name: str
    description: str
    system_prompt: str

    async def run(self, state: dict) -> dict:
        challenge = state["challenge"]
        domain = state.get("domain", "").strip()
        focus_areas = state.get("focus_areas", [])
        key_questions = state.get("key_questions", [])

        focus_text = "\n".join(f"- {f}" for f in focus_areas) if focus_areas else "General analysis"
        questions_text = "\n".join(f"- {q}" for q in key_questions) if key_questions else ""
        company_url = domain if domain.startswith("http") else (f"https://{domain}" if domain else "")

        research_instruction = """
This is a DOMAIN-BASED company analysis. You have access to the live public web.
You MUST research the company before making findings.
1. Inspect the company's official website first using URL context.
2. Use Google Search for external evidence relevant to your specialist role: competitors, pricing, customer signals, market trends, reviews, channels, recent announcements, or other public evidence as appropriate.
3. Separate OBSERVED facts from INFERENCES. Never present an inference as a verified fact.
4. If public evidence is insufficient, say so explicitly in data_gaps rather than inventing metrics.
5. Prefer recent, primary, and company-specific sources. Do not rely only on generic industry knowledge.
""" if company_url else """
No company domain was supplied. Treat this as a hypothesis-driven analysis and clearly label assumptions. Do not invent company-specific facts.
"""

        user_message = f"""Business challenge: "{challenge}"

Company domain: {domain or "not provided"}
Official company URL: {company_url or "not provided"}

Your specific focus areas:
{focus_text}

Key diagnostic questions to address:
{questions_text}

{research_instruction}

Return JSON with this structure:
{{
  "findings": [
    {{
      "finding": "<specific finding>",
      "significance": "<high|medium|low>",
      "evidence": "<what was observed and why it matters>",
      "evidence_type": "<observed|inferred>",
      "source_urls": ["<source URL>"]
    }}
  ],
  "insights": [
    {{"insight": "<actionable insight>", "confidence": <0.0-1.0>, "source_urls": ["<source URL>"]}}
  ],
  "risks": ["<risk 1>"],
  "opportunities": ["<opportunity 1>"],
  "data_gaps": ["<specific missing evidence that would improve the conclusion>"],
  "search_queries": ["<important query actually used>"]
}}

Quality bar:
- Minimum 3 substantive findings and 2 insights.
- Findings must be company-specific whenever a domain is supplied.
- Do not fill space with generic advice.
- Do not fabricate revenue, market share, customer counts, pricing, competitors, or performance metrics.
- Quantify only when a public source supports the number.
"""

        tools = []
        if company_url:
            tools.append({"url_context": {}})
            tools.append({"google_search": {}})

        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            response_mime_type="application/json",
            tools=tools or None,
        )

        response = await _client.aio.models.generate_content(
            model=_MODEL,
            contents=user_message,
            config=config,
        )
        result = json.loads(response.text)
        result["agent"] = self.name

        # Persist the actual grounding sources returned by Gemini alongside the agent result.
        sources: list[dict[str, str]] = []
        try:
            metadata = response.candidates[0].grounding_metadata
            for chunk in metadata.grounding_chunks or []:
                if chunk.web and chunk.web.uri:
                    sources.append({"title": chunk.web.title or "Web source", "url": chunk.web.uri})
        except (AttributeError, IndexError, TypeError):
            pass
        if sources:
            result["grounding_sources"] = sources

        return {
            "agent_results": {self.name: result},
            "progress": [
                f"{self.name} intelligence complete — {len(result.get('findings', []))} findings"
                + (f" · {len(sources)} web sources" if sources else "")
            ],
        }

    @abstractmethod
    def _get_system_prompt(self) -> str: ...
