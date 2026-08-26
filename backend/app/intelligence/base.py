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
        focus_areas = state.get("focus_areas", [])
        key_questions = state.get("key_questions", [])

        focus_text = "\n".join(f"- {f}" for f in focus_areas) if focus_areas else "General analysis"
        questions_text = "\n".join(f"- {q}" for q in key_questions) if key_questions else ""

        user_message = f"""Business challenge: "{challenge}"

Your specific focus areas:
{focus_text}

Key diagnostic questions to address:
{questions_text}

Provide your intelligence analysis as JSON with this structure:
{{
  "findings": [
    {{"finding": "<key finding>", "significance": "<high|medium|low>", "evidence": "<supporting reasoning>"}}
  ],
  "insights": [
    {{"insight": "<actionable insight>", "confidence": <0.0-1.0>}}
  ],
  "risks": ["<risk 1>", "<risk 2>"],
  "opportunities": ["<opportunity 1>", "<opportunity 2>"],
  "data_gaps": ["<what additional data would improve this analysis>"]
}}

Be specific, analytical, and grounded. Minimum 3 findings and 2 insights."""

        response = await _client.aio.models.generate_content(
            model=_MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                response_mime_type="application/json",
            ),
        )
        result = json.loads(response.text)
        result["agent"] = self.name

        return {
            "agent_results": {self.name: result},
            "progress": [f"{self.name} intelligence complete — {len(result.get('findings', []))} findings"],
        }

    @abstractmethod
    def _get_system_prompt(self) -> str: ...
