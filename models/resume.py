from pydantic import BaseModel
from typing import List

class ResumeAnalysis(BaseModel):
    """Resume analysis result model."""
    candidate_name: str
    education: List[str]
    skills: List[str]
    experience_summary: str
    strengths: List[str]
    improvement_areas: List[str]
    recommended_job_roles: List[str]
