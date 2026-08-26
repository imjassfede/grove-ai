import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_session
from app.database.repositories import AnalysisRepository
from app.reasoning.state import GrowthState
from app.schemas.requests import SubmitChallengeRequest
from app.schemas.responses import AnalysisListResponse, AnalysisResponse

router = APIRouter(prefix="/analyses", tags=["analyses"])


# ── Background task ────────────────────────────────────────────────────────────

async def _run_graph(analysis_id: uuid.UUID, challenge: str) -> None:
    """Runs entirely outside the request session — creates its own DB session."""
    from app.database.connection import _SessionLocal
    from app.reasoning.orchestrator import graph

    async with _SessionLocal() as session:
        repo = AnalysisRepository(session)
        await repo.update_from_state(analysis_id, {"status": "running", "progress": ["Starting analysis…"]})

        initial_state: GrowthState = {
            "challenge": challenge,
            "analysis_id": str(analysis_id),
            "business_area": "",
            "problem_type": "",
            "urgency": "",
            "key_questions": [],
            "selected_agents": [],
            "agent_focus": {},
            "agent_results": {},
            "root_causes": [],
            "insights": [],
            "recommendations": [],
            "experiments": [],
            "executive_summary": "",
            "status": "classifying",
            "progress": [],
            "error": None,
        }

        try:
            async for event in graph.astream(initial_state):
                for _node, state_update in event.items():
                    if isinstance(state_update, dict):
                        await repo.update_from_state(analysis_id, state_update)
        except Exception as exc:
            await repo.update_from_state(analysis_id, {"status": "error", "error": str(exc)})


# ── Routes ─────────────────────────────────────────────────────────────────────

@router.post("", response_model=AnalysisResponse, status_code=201)
async def submit_challenge(
    request: SubmitChallengeRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
) -> AnalysisResponse:
    """Create an analysis and immediately kick off the AI reasoning pipeline."""
    repo = AnalysisRepository(session)
    analysis = await repo.create(request.challenge)
    background_tasks.add_task(_run_graph, analysis.id, analysis.challenge)
    return AnalysisResponse.model_validate(analysis)


@router.get("", response_model=AnalysisListResponse)
async def list_analyses(session: AsyncSession = Depends(get_session)) -> AnalysisListResponse:
    repo = AnalysisRepository(session)
    analyses = await repo.list_all()
    return AnalysisListResponse(
        analyses=[AnalysisResponse.model_validate(a) for a in analyses],
        total=len(analyses),
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> AnalysisResponse:
    repo = AnalysisRepository(session)
    analysis = await repo.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisResponse.model_validate(analysis)
