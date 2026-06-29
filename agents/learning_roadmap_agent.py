import json
import logging
from google import genai
from config import settings
from models.career_advice import CareerAdvice
from models.learning_roadmap import LearningRoadmap
from pathlib import Path

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.google_api_key)

async def get_learning_roadmap(advice: CareerAdvice) -> LearningRoadmap:
    """Get learning roadmap using Gemini."""
    prompt_path = Path("prompts/learning_roadmap.txt")
    
    if not prompt_path.exists():
        logger.error(f"Prompt file not found at {prompt_path}")
        raise FileNotFoundError(f"Prompt file not found at {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        career_advice=advice.model_dump_json()
    )
    
    try:
        response = client.models.generate_content(
            model=settings.model_name,
            contents=prompt,
        )
        
        # Parse JSON from response
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        
        data = json.loads(response_text)
        return LearningRoadmap(**data)
        
    except Exception as e:
        logger.error(f"Error getting learning roadmap from Gemini: {e}")
        raise ValueError("Failed to get learning roadmap")
