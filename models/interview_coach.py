from pydantic import BaseModel
from typing import List

class InterviewQuestion(BaseModel):
    """Interview question model."""
    question: str
    sample_answer: str

class InterviewCoach(BaseModel):
    """Interview coach model."""
    target_role: str
    technical_questions: List[InterviewQuestion]
    behavioral_questions: List[InterviewQuestion]
    resume_questions: List[InterviewQuestion]
    tips: List[str]
