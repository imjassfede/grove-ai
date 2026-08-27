import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.database.models import AuthSession, User, UserProfile
from app.integrations.growth import track_event

router = APIRouter(prefix="/profile", tags=["profile"])

class ProfileUpdate(BaseModel):
    first_name: str | None = Field(default=None, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)
    role: str | None = Field(default=None, max_length=120)
    company: str | None = Field(default=None, max_length=160)
    website: str | None = Field(default=None, max_length=255)
    goals: list[str] = Field(default_factory=list, max_length=10)
    interests: list[str] = Field(default_factory=list, max_length=12)
    onboarding_completed: bool | None = None

class ProfileResponse(BaseModel):
    id: str; email: str; first_name: str | None; last_name: str | None; credits: int
    role: str | None; company: str | None; website: str | None; goals: list[str]; interests: list[str]; onboarding_completed: bool

async def _current_user(session: AsyncSession, cookie_token: str | None, authorization: str | None) -> User:
    token = cookie_token
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    if not token: raise HTTPException(status_code=401, detail="Not authenticated")
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    result = await session.execute(select(AuthSession).where(AuthSession.token_hash == token_hash, AuthSession.expires_at > datetime.now(timezone.utc)))
    auth_session = result.scalar_one_or_none()
    if not auth_session: raise HTTPException(status_code=401, detail="Not authenticated")
    user = await session.get(User, auth_session.user_id)
    if not user: raise HTTPException(status_code=401, detail="Not authenticated")
    return user

async def _get_profile(session: AsyncSession, user: User) -> UserProfile:
    result = await session.execute(select(UserProfile).where(UserProfile.user_id == user.id)); profile = result.scalar_one_or_none()
    if profile: return profile
    profile = UserProfile(user_id=user.id, goals=[], interests=[]); session.add(profile); await session.commit(); await session.refresh(profile); return profile

def _response(user: User, profile: UserProfile) -> ProfileResponse:
    return ProfileResponse(id=str(profile.id), email=user.email, first_name=user.first_name, last_name=user.last_name, credits=user.credits, role=profile.role, company=profile.company, website=profile.website, goals=profile.goals or [], interests=profile.interests or [], onboarding_completed=profile.onboarding_completed)

@router.get("", response_model=ProfileResponse)
async def get_profile(grove_session: str | None = Cookie(default=None), authorization: str | None = Header(default=None), session: AsyncSession = Depends(get_session)):
    user = await _current_user(session, grove_session, authorization); return _response(user, await _get_profile(session, user))

@router.patch("", response_model=ProfileResponse)
async def update_profile(request: ProfileUpdate, grove_session: str | None = Cookie(default=None), authorization: str | None = Header(default=None), session: AsyncSession = Depends(get_session)):
    user = await _current_user(session, grove_session, authorization); profile = await _get_profile(session, user); data = request.model_dump(exclude_unset=True)
    if "first_name" in request.model_fields_set: user.first_name = data.pop("first_name")
    if "last_name" in request.model_fields_set: user.last_name = data.pop("last_name")
    for key, value in data.items(): setattr(profile, key, value)
    await session.commit(); await session.refresh(user); await session.refresh(profile)
    if profile.onboarding_completed: await track_event("profile_completed", str(user.id))
    return _response(user, profile)
