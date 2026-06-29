from pydantic import BaseModel
from typing import List
from models.job import Job

class JobMatch(BaseModel):
    """Job match result."""
    job: Job
    score: int
    reason: str

class JobMatchResponse(BaseModel):
    """Job match API response."""
    candidate_name: str
    matches: List[JobMatch]
