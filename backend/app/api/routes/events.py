import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.database.models import ProductEvent
from app.integrations.growth import track_event

router = APIRouter(prefix="/events", tags=["events"])


class EventRequest(BaseModel):
    event_name: str = Field(min_length=2, max_length=80)
    anonymous_id: str | None = Field(default=None, max_length=120)
    user_id: uuid.UUID | None = None
    properties: dict = Field(default_factory=dict)


@router.post("", status_code=202)
async def create_event(request: EventRequest, session: AsyncSession = Depends(get_session)):
    event = ProductEvent(event_name=request.event_name, anonymous_id=request.anonymous_id, user_id=request.user_id, properties=request.properties)
    session.add(event)
    await session.commit()
    await track_event(request.event_name, str(request.user_id or request.anonymous_id or "anonymous"), request.properties)
    return {"accepted": True}
