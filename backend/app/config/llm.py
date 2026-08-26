from google import genai
from google.genai import types

from app.config.settings import get_settings

_client = genai.Client(api_key=get_settings().google_api_key)
_MODEL = "gemini-2.0-flash"


async def complete(system: str, user: str) -> dict:
    """Single async JSON-mode call to Gemini Flash. Returns parsed dict."""
    import json

    response = await _client.aio.models.generate_content(
        model=_MODEL,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)
