import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import create_session, get_user_by_email, hash_password, verify_password
from app.database.connection import get_session
from app.database.models import AuthSession, User
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str | None = Field(default=None, max_length=80)
    last_name: str | None = Field(default=None, max_length=80)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    id: str
    email: str
    first_name: str | None
    last_name: str | None
    credits: int


def _response(user: User) -> AuthResponse:
    return AuthResponse(id=str(user.id), email=user.email, first_name=user.first_name, last_name=user.last_name, credits=user.credits)


async def _set_session(response: Response, session: AsyncSession, user: User) -> AuthResponse:
    token = await create_session(session, user)
    response.set_cookie("grove_session", token, httponly=True, secure=False, samesite="lax", max_age=30 * 86400, path="/")
    return _response(user)


@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(request: SignupRequest, response: Response, session: AsyncSession = Depends(get_session)):
    email = str(request.email).lower()
    if await get_user_by_email(session, email):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(email=email, password_hash=hash_password(request.password), first_name=request.first_name, last_name=request.last_name, credits=5)
    session.add(user)
    await session.flush()
    await session.commit()
    return await _set_session(response, session, user)


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, response: Response, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, str(request.email).lower())
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return await _set_session(response, session, user)


@router.post("/logout", status_code=204)
async def logout(response: Response, grove_session: str | None = Cookie(default=None), session: AsyncSession = Depends(get_session)):
    if grove_session:
        token_hash = hashlib.sha256(grove_session.encode()).hexdigest()
        result = await session.execute(select(AuthSession).where(AuthSession.token_hash == token_hash))
        auth_session = result.scalar_one_or_none()
        if auth_session:
            await session.delete(auth_session)
            await session.commit()
    response.delete_cookie("grove_session", path="/")


@router.get("/me", response_model=AuthResponse)
async def me(grove_session: str | None = Cookie(default=None), session: AsyncSession = Depends(get_session)):
    if not grove_session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token_hash = hashlib.sha256(grove_session.encode()).hexdigest()
    result = await session.execute(select(AuthSession).where(AuthSession.token_hash == token_hash, AuthSession.expires_at > datetime.now(timezone.utc)))
    auth_session = result.scalar_one_or_none()
    if not auth_session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = await session.get(User, auth_session.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return _response(user)
