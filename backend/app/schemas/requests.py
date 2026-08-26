from pydantic import BaseModel, Field


class SubmitChallengeRequest(BaseModel):
    challenge: str = Field(..., min_length=10, max_length=2000, description="The business challenge to analyze")
