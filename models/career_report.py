from pydantic import BaseModel
from models.career_advice import CareerAdvice
from models.learning_roadmap import LearningRoadmap
from models.interview_coach import InterviewCoach

class CareerReport(BaseModel):
    """Unified career report model."""
    candidate_name: str
    career_advice: CareerAdvice
    learning_roadmap: LearningRoadmap
    interview_preparation: InterviewCoach
    overall_summary: str
