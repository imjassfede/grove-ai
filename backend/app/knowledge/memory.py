from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories import AnalysisRepository


class AnalysisMemory:
    """Retrieves prior analyses to inform current reasoning."""

    def __init__(self, session: AsyncSession):
        self.repo = AnalysisRepository(session)

    async def get_similar_analyses(self, challenge: str, limit: int = 3) -> list[dict]:
        analyses = await self.repo.list_all(limit=20)
        # TODO: replace with vector similarity search via pgvector
        return [
            {
                "challenge": a.challenge,
                "business_area": a.business_area,
                "executive_summary": a.executive_summary,
            }
            for a in analyses[:limit]
            if a.status == "complete"
        ]
