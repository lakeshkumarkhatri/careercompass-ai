import logging
from pathlib import Path
from typing import Type, TypeVar
from pydantic import BaseModel
from services.gemini_service import generate_json

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)

class BaseAgent:
    """Base class for all AI agents."""

    def __init__(self, prompt_file: str):
        self.prompt_path = Path(prompt_file)
        if not self.prompt_path.exists():
            logger.error(f"Prompt file not found at {self.prompt_path}")
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")

    def _load_prompt_template(self) -> str:
        """Load prompt template from file."""
        return self.prompt_path.read_text(encoding="utf-8")

    async def generate(self, response_model: Type[T], replacements: dict[str, str]) -> T:
        """Generate structured response using Gemini."""
        prompt_template = self._load_prompt_template()
        
        # Replace tokens
        prompt = prompt_template
        for key, value in replacements.items():
            prompt = prompt.replace(f"<<{key}>>", value)
            
        try:
            return await generate_json(prompt, response_model)
        except Exception as e:
            logger.error(f"Agent {self.__class__.__name__} generation failed: {e}")
            raise
