import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, String, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    challenge: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending")

    # Reasoning outputs
    business_area: Mapped[str | None] = mapped_column(String(64))
    problem_type: Mapped[str | None] = mapped_column(String(64))
    urgency: Mapped[str | None] = mapped_column(String(16))
    selected_agents: Mapped[list | None] = mapped_column(JSON)

    # Intelligence outputs
    agent_results: Mapped[dict | None] = mapped_column(JSON)

    # Synthesis outputs
    root_causes: Mapped[list | None] = mapped_column(JSON)
    insights: Mapped[list | None] = mapped_column(JSON)
    recommendations: Mapped[list | None] = mapped_column(JSON)
    experiments: Mapped[list | None] = mapped_column(JSON)
    executive_summary: Mapped[str | None] = mapped_column(Text)

    # Progress log
    progress: Mapped[list | None] = mapped_column(JSON)
    error: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
