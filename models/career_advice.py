from pydantic import BaseModel
from typing import List

class CareerAdvice(BaseModel):
    """Career advice model."""
    candidate_name: str
    career_path: str
    summary: str
    top_strengths: List[str]
    skill_gaps: List[str]
    recommended_jobs: List[str]
    next_steps: List[str]
