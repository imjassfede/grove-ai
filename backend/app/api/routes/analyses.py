import hashlib
import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Cookie, Depends, Header, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.database.models import AnonymousSession, AuthSession, Analysis, User
from app.database.repositories import AnalysisRepository
from app.integrations.growth import track_event
from app.knowledge.memory import AnalysisMemory
from app.reasoning.state import GrowthState
from app.schemas.requests import SubmitChallengeRequest
from app.schemas.responses import AnalysisListResponse, AnalysisResponse

router = APIRouter(prefix="/analyses", tags=["analyses"]); ANON_COOKIE = "grove_anonymous"; FREE_CREDITS = 5
logger = logging.getLogger(__name__)
PUBLIC_ANALYSIS_ERROR = "Analysis temporarily unavailable. Please try again later."

async def _run_graph(analysis_id: uuid.UUID, challenge: str, domain: str | None = None) -> None:
    from app.database.connection import _SessionLocal
    from app.reasoning.orchestrator import graph
    async with _SessionLocal() as session:
        repo = AnalysisRepository(session); await repo.update_from_state(analysis_id, {"status": "running", "progress": ["Starting grounded growth investigation…"]}); prior_memory = await AnalysisMemory(session).get_similar_analyses(challenge, limit=3)
        initial_state: GrowthState = {"challenge": challenge, "analysis_id": str(analysis_id), "domain": domain or "", "business_area": "", "problem_type": "", "urgency": "", "key_questions": [], "selected_agents": [], "agent_focus": {}, "agent_results": {}, "agent_trace": {}, "knowledge_graph": {"nodes": [], "edges": []}, "research_memory": prior_memory, "critic": {}, "research_round": 0, "followup_agent": None, "followup_focus": "", "root_causes": [], "insights": [], "recommendations": [], "experiments": [], "executive_summary": "", "status": "classifying", "progress": [], "error": None}
        try:
            async for event in graph.astream(initial_state):
                for _node, state_update in event.items():
                    if isinstance(state_update, dict): await repo.update_from_state(analysis_id, state_update)
            await track_event("analysis_completed", str(analysis_id), {"analysis_id": str(analysis_id)})
        except Exception:
            logger.exception("Analysis pipeline failed", extra={"analysis_id": str(analysis_id)})
            await repo.update_from_state(analysis_id, {"status": "error", "error": PUBLIC_ANALYSIS_ERROR, "progress": ["Analysis could not be completed."]})
            try:
                await track_event("analysis_failed", str(analysis_id), {"analysis_id": str(analysis_id)})
            except Exception:
                logger.exception("Failed to track analysis failure", extra={"analysis_id": str(analysis_id)})

async def _get_or_create_anonymous(session: AsyncSession, token: str | None) -> tuple[AnonymousSession, str]:
    if token:
        token_hash = hashlib.sha256(token.encode()).hexdigest(); result = await session.execute(select(AnonymousSession).where(AnonymousSession.token_hash == token_hash, AnonymousSession.expires_at > datetime.now(timezone.utc))); existing = result.scalar_one_or_none()
        if existing: return existing, token
    raw = secrets.token_urlsafe(32); anon = AnonymousSession(token_hash=hashlib.sha256(raw.encode()).hexdigest(), credits=FREE_CREDITS, expires_at=datetime.now(timezone.utc) + timedelta(days=30)); session.add(anon); await session.flush(); return anon, raw

async def _get_authenticated_user(session: AsyncSession, cookie_token: str | None, authorization: str | None) -> User | None:
    token = cookie_token
    if authorization and authorization.lower().startswith("bearer "): token = authorization[7:].strip()
    if not token: return None
    token_hash = hashlib.sha256(token.encode()).hexdigest(); result = await session.execute(select(AuthSession).where(AuthSession.token_hash == token_hash, AuthSession.expires_at > datetime.now(timezone.utc))); auth = result.scalar_one_or_none()
    return await session.get(User, auth.user_id) if auth else None

@router.post("", response_model=AnalysisResponse, status_code=201)
async def submit_challenge(request: SubmitChallengeRequest, response: Response, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session), grove_session: str | None = Cookie(default=None), grove_anonymous: str | None = Cookie(default=None), authorization: str | None = Header(default=None)) -> AnalysisResponse:
    user = await _get_authenticated_user(session, grove_session, authorization)
    if user:
        if user.credits < 1: raise HTTPException(status_code=402, detail="No Grove credits remaining")
        user.credits -= 1; analysis = Analysis(challenge=request.challenge, domain=request.domain, user_id=user.id, status="pending"); session.add(analysis); await session.commit(); await session.refresh(analysis); await track_event("credit_consumed", str(user.id), {"analysis_id": str(analysis.id), "credits_remaining": user.credits})
    else:
        anon, raw_token = await _get_or_create_anonymous(session, grove_anonymous)
        if anon.credits < 1: raise HTTPException(status_code=402, detail="Your 5 free credits have been used. Create an account to continue.")
        anon.credits -= 1; analysis = Analysis(challenge=request.challenge, domain=request.domain, anonymous_session_id=anon.id, status="pending"); session.add(analysis); await session.commit(); await session.refresh(analysis); response.set_cookie(ANON_COOKIE, raw_token, httponly=True, secure=True, samesite="none", max_age=30 * 86400, path="/"); await track_event("credit_consumed", "anonymous", {"analysis_id": str(analysis.id), "anonymous": True, "credits_remaining": anon.credits})
    background_tasks.add_task(_run_graph, analysis.id, analysis.challenge, analysis.domain); return AnalysisResponse.model_validate(analysis)

@router.get("", response_model=AnalysisListResponse)
async def list_analyses(session: AsyncSession = Depends(get_session), grove_session: str | None = Cookie(default=None), authorization: str | None = Header(default=None)) -> AnalysisListResponse:
    user = await _get_authenticated_user(session, grove_session, authorization)
    if not user: raise HTTPException(status_code=401, detail="Not authenticated")
    result = await session.execute(select(Analysis).where(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()).limit(50)); analyses = list(result.scalars().all()); return AnalysisListResponse(analyses=[AnalysisResponse.model_validate(a) for a in analyses], total=len(analyses))

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: uuid.UUID, session: AsyncSession = Depends(get_session), grove_session: str | None = Cookie(default=None), grove_anonymous: str | None = Cookie(default=None), authorization: str | None = Header(default=None)) -> AnalysisResponse:
    analysis = await session.get(Analysis, analysis_id)
    if not analysis: raise HTTPException(status_code=404, detail="Analysis not found")
    user = await _get_authenticated_user(session, grove_session, authorization)
    if user and analysis.user_id == user.id: return AnalysisResponse.model_validate(analysis)
    if analysis.user_id is None and grove_anonymous:
        token_hash = hashlib.sha256(grove_anonymous.encode()).hexdigest(); result = await session.execute(select(AnonymousSession).where(AnonymousSession.token_hash == token_hash)); anon = result.scalar_one_or_none()
        if anon and analysis.anonymous_session_id == anon.id: return AnalysisResponse.model_validate(analysis)
    raise HTTPException(status_code=403, detail="You do not have access to this analysis")
