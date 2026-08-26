import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Analysis


class AnalysisRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, challenge: str) -> Analysis:
        analysis = Analysis(challenge=challenge, status="pending")
        self.session.add(analysis)
        await self.session.commit()
        await self.session.refresh(analysis)
        return analysis

    async def get(self, analysis_id: uuid.UUID) -> Analysis | None:
        result = await self.session.execute(select(Analysis).where(Analysis.id == analysis_id))
        return result.scalar_one_or_none()

    async def list_all(self, limit: int = 50) -> list[Analysis]:
        result = await self.session.execute(
            select(Analysis).order_by(Analysis.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def update_from_state(self, analysis_id: uuid.UUID, state: dict) -> Analysis | None:
        analysis = await self.get(analysis_id)
        if not analysis:
            return None

        fields = [
            "status", "business_area", "problem_type", "urgency",
            "selected_agents", "agent_results", "root_causes",
            "insights", "recommendations", "experiments",
            "executive_summary", "progress", "error",
        ]
        for field in fields:
            if field in state:
                setattr(analysis, field, state[field])

        analysis.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(analysis)
        return analysis
