from agents.base_agent import BaseAgent
from models.resume import ResumeAnalysis
from models.job_match import JobMatchResponse
from models.career_advice import CareerAdvice
from models.interview_coach import InterviewCoach

class InterviewCoachAgent(BaseAgent):
    """Agent to provide interview coaching."""

    def __init__(self):
        super().__init__("prompts/interview_coach.txt")

    async def get_coaching(self, analysis: ResumeAnalysis, matches: JobMatchResponse, advice: CareerAdvice) -> InterviewCoach:
        """Get interview coaching using Gemini."""
        replacements = {
            "CANDIDATE_PROFILE": analysis.model_dump_json(),
            "JOB_MATCHES": matches.model_dump_json(),
            "CAREER_ADVICE": advice.model_dump_json()
        }
        return await self.generate(InterviewCoach, replacements)
