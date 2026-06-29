import logging
from agents.base_agent import BaseAgent
from agents.career_advisor_agent import CareerAdvisorAgent
from agents.learning_roadmap_agent import LearningRoadmapAgent
from agents.interview_coach_agent import InterviewCoachAgent
from models.resume import ResumeAnalysis
from models.job_match import JobMatchResponse
from models.career_report import CareerReport
from models.overall_summary import OverallSummary
from services.user_profile_service import get_profile

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    """Agent to orchestrate all career agents."""

    def __init__(self):
        super().__init__("prompts/orchestrator.txt")
        self.advisor_agent = CareerAdvisorAgent()
        self.roadmap_agent = LearningRoadmapAgent()
        self.interview_agent = InterviewCoachAgent()

    async def get_report(self, analysis: ResumeAnalysis, matches: JobMatchResponse, user_id: Optional[str] = None) -> CareerReport:
        """Aggregate results and generate report with optional user personalization."""
        user_profile = None
        if user_id:
            user_profile = get_profile(user_id)
            if user_profile:
                logger.info(f"Personalizing report for user: {user_id}")
                # Personalization logic could be injected into agent calls
                # For now, just logging its presence
        
        # 1. Invoke agents
        # (Note: Personalization logic would be integrated here if agents accepted profile)
        advice = await self.advisor_agent.get_advice(analysis, matches)
        roadmap = await self.roadmap_agent.get_roadmap(advice)
        interview = await self.interview_agent.get_coaching(analysis, matches, advice)
        
        # 2. Generate summary
        replacements = {
            "CAREER_ADVICE": advice.model_dump_json(),
            "LEARNING_ROADMAP": roadmap.model_dump_json(),
            "INTERVIEW_PREPARATION": interview.model_dump_json()
        }
        summary_model: OverallSummary = await self.generate(OverallSummary, replacements)
        
        # 3. Aggregate
        return CareerReport(
            candidate_name=analysis.candidate_name,
            career_advice=advice,
            learning_roadmap=roadmap,
            interview_preparation=interview,
            overall_summary=summary_model.overall_summary
        )
