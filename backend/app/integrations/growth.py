import asyncio
import uuid

import httpx

from app.config.settings import get_settings


def _posthog_event(event_name: str, distinct_id: str, properties: dict) -> None:
    settings = get_settings()
    if not settings.posthog_api_key:
        return
    try:
        httpx.post(
            f"{settings.posthog_host}/capture/",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {settings.posthog_api_key}"},
            json={"api_key": settings.posthog_api_key, "event": event_name, "distinct_id": distinct_id, "properties": {"$lib": "grove", **properties}},
            timeout=5,
        )
    except Exception:
        pass


def _brevo_contact(email: str, first_name: str | None, last_name: str | None, attributes: dict) -> None:
    settings = get_settings()
    if not settings.brevo_api_key or not settings.brevo_list_id:
        return
    try:
        httpx.post(
            "https://api.brevo.com/v3/contacts",
            headers={"accept": "application/json", "content-type": "application/json", "api-key": settings.brevo_api_key},
            json={"email": email, "attributes": {"FIRSTNAME": first_name or "", "LASTNAME": last_name or "", **attributes}, "listIds": [settings.brevo_list_id], "updateEnabled": True},
            timeout=5,
        )
    except Exception:
        pass


def _n8n_event(event_name: str, payload: dict) -> None:
    settings = get_settings()
    if not settings.n8n_webhook_url:
        return
    try:
        httpx.post(settings.n8n_webhook_url, json={"event": event_name, "payload": payload}, timeout=5)
    except Exception:
        pass


async def track_event(event_name: str, distinct_id: str, properties: dict | None = None) -> None:
    props = properties or {}
    await asyncio.to_thread(_posthog_event, event_name, distinct_id, props)
    await asyncio.to_thread(_n8n_event, event_name, {"distinct_id": distinct_id, **props})


async def sync_lead(email: str, first_name: str | None, last_name: str | None, user_id: uuid.UUID, properties: dict | None = None) -> None:
    props = properties or {}
    await asyncio.to_thread(_brevo_contact, email, first_name, last_name, {"GROVE_USER_ID": str(user_id), **props})
    await track_event("lead_synced", str(user_id), {"email": email, **props})
