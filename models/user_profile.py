from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    """User profile model."""
    user_id: str
    email: str
    career_goals: str
    skills: List[str]
    completed_courses: List[str]
    preferences: dict
