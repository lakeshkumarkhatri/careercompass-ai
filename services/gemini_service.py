import json
import logging
from google import genai
from config import settings
from models.resume import ResumeAnalysis
from pydantic import BaseModel
from typing import Type, TypeVar

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.google_api_key)

T = TypeVar("T", bound=BaseModel)

def load_prompt(file_path: str) -> str:
    """Load prompt template from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

async def generate_json(prompt: str, response_model: Type[T]) -> T:
    """Generic Gemini call to generate structured JSON."""
    try:
        response = client.models.generate_content(
            model=settings.model_name,
            contents=prompt,
        )
        
        # Parse JSON from response
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3].strip()
        elif response_text.startswith("```"):
            response_text = response_text[3:-3].strip()
        
        data = json.loads(response_text)
        return response_model(**data)
        
    except Exception as e:
        logger.error(f"Error generating content with Gemini: {e}")
        raise ValueError(f"Failed to generate content: {e}")

async def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """Analyze resume using Gemini."""
    prompt_template = load_prompt("prompts/resume_analysis.txt")
    prompt = prompt_template.format(resume_text=resume_text)
    return await generate_json(prompt, ResumeAnalysis)
