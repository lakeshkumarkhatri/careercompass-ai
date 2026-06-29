from agents.base_agent import BaseAgent
from models.career_advice import CareerAdvice
from models.learning_roadmap import LearningRoadmap

class LearningRoadmapAgent(BaseAgent):
    """Agent to provide learning roadmap."""

    def __init__(self):
        super().__init__("prompts/learning_roadmap.txt")

    async def get_roadmap(self, advice: CareerAdvice) -> LearningRoadmap:
        """Get learning roadmap using Gemini."""
        replacements = {
            "CAREER_ADVICE": advice.model_dump_json()
        }
        return await self.generate(LearningRoadmap, replacements)

async def get_learning_roadmap(advice: CareerAdvice) -> LearningRoadmap:
    """Convenience wrapper."""
    agent = LearningRoadmapAgent()
    return await agent.get_roadmap(advice)
