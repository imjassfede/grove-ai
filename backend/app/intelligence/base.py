import json
from abc import ABC, abstractmethod

import anthropic

from app.config.settings import get_settings

_client = anthropic.AsyncAnthropic(api_key=get_settings().anthropic_api_key)


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

        response = await _client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=[{
                "type": "text",
                "text": self.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_message}],
        )

        result = json.loads(response.content[0].text)
        result["agent"] = self.name

        return {
            "agent_results": {self.name: result},
            "progress": [f"{self.name} intelligence complete — {len(result.get('findings', []))} findings"],
        }

    @abstractmethod
    def _get_system_prompt(self) -> str: ...
