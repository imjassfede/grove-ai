import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenge: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending")  # pending|running|complete|error

    # Reasoning outputs
    business_area: Mapped[str | None] = mapped_column(String(64))
    problem_type: Mapped[str | None] = mapped_column(String(64))
    urgency: Mapped[str | None] = mapped_column(String(16))
    selected_agents: Mapped[list | None] = mapped_column(JSONB)

    # Intelligence outputs
    agent_results: Mapped[dict | None] = mapped_column(JSONB)

    # Synthesis outputs
    root_causes: Mapped[list | None] = mapped_column(JSONB)
    insights: Mapped[list | None] = mapped_column(JSONB)
    recommendations: Mapped[list | None] = mapped_column(JSONB)
    experiments: Mapped[list | None] = mapped_column(JSONB)
    executive_summary: Mapped[str | None] = mapped_column(Text)

    # Progress log
    progress: Mapped[list | None] = mapped_column(JSONB)
    error: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
