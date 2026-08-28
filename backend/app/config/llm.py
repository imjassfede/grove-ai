import json

from google import genai
from google.genai import types

from app.config.settings import get_settings

_client = genai.Client(api_key=get_settings().google_api_key)
# Keep every LLM entry point on the currently supported model.
_MODEL = "gemini-3.6-flash"


async def complete(system: str, user: str) -> dict:
    """Single async JSON-mode call to Gemini Flash. Returns parsed dict."""
    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)
