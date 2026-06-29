from agents.base_agent import BaseAgent
from models.resume import ResumeAnalysis
from models.job_match import JobMatchResponse
from models.career_advice import CareerAdvice

class CareerAdvisorAgent(BaseAgent):
    """Agent to provide career advice."""

    def __init__(self):
        super().__init__("prompts/career_advisor.txt")

    async def get_advice(self, analysis: ResumeAnalysis, matches: JobMatchResponse) -> CareerAdvice:
        """Get career advice using Gemini."""
        replacements = {
            "CANDIDATE_NAME": analysis.candidate_name,
            "RESUME_SUMMARY": analysis.experience_summary,
            "JOB_MATCHES": matches.model_dump_json()
        }
        return await self.generate(CareerAdvice, replacements)

async def get_career_advice(analysis: ResumeAnalysis, matches: JobMatchResponse) -> CareerAdvice:
    """Convenience wrapper."""
    agent = CareerAdvisorAgent()
    return await agent.get_advice(analysis, matches)
