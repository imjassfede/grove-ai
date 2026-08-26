from __future__ import annotations

import httpx
from app.config.settings import get_settings


async def sync_lead_to_brevo(email: str, first_name: str | None, last_name: str | None, user_id: str, source: str | None = None) -> bool:
    settings = get_settings()
    if not settings.brevo_api_key:
        return False
    attributes = {"GROVE_USER_ID": user_id, "LIFECYCLE": "signup", "SOURCE": source or "organic"}
    if first_name:
        attributes["FIRSTNAME"] = first_name
    if last_name:
        attributes["LASTNAME"] = last_name
    payload = {"email": email, "attributes": attributes, "updateEnabled": True}
    if settings.brevo_list_id:
        payload["listIds"] = [settings.brevo_list_id]
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post("https://api.brevo.com/v3/contacts", headers={"api-key": settings.brevo_api_key, "Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
    return True
