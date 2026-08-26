from pydantic import BaseModel, Field


class SubmitChallengeRequest(BaseModel):
    challenge: str = Field(..., min_length=10, max_length=2000, description="The business challenge to analyze")
    domain: str | None = Field(default=None, min_length=3, max_length=255, description="Company domain used to seed a company analysis")
