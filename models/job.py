from pydantic import BaseModel
from typing import List

class Job(BaseModel):
    """Job model."""
    id: str
    title: str
    company: str
    skills: List[str]
