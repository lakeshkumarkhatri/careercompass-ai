from pydantic import BaseModel
from typing import List

class Roadmap(BaseModel):
    """30/60/90 day roadmap."""
    thirty_days: List[str]
    sixty_days: List[str]
    ninety_days: List[str]

class LearningRoadmap(BaseModel):
    """Learning roadmap model."""
    career_goal: str
    roadmap: Roadmap
    recommended_courses: List[str]
    recommended_projects: List[str]
    recommended_certifications: List[str]
