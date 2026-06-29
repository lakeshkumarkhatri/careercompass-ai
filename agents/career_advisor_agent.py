import json
import logging
from google import genai
from config import settings
from models.resume import ResumeAnalysis
from models.job_match import JobMatchResponse
from models.career_advice import CareerAdvice
from pathlib import Path

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.google_api_key)

async def get_career_advice(analysis: ResumeAnalysis, matches: JobMatchResponse) -> CareerAdvice:
    """Get career advice using Gemini."""
    prompt_path = Path("prompts/career_advisor.txt")
    
    if not prompt_path.exists():
        logger.error(f"Prompt file not found at {prompt_path}")
        raise FileNotFoundError(f"Prompt file not found at {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        candidate_name=analysis.candidate_name,
        resume_summary=analysis.experience_summary,
        job_matches=matches.model_dump_json()
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
        return CareerAdvice(**data)
        
    except Exception as e:
        logger.error(f"Error getting career advice from Gemini: {e}")
        raise ValueError("Failed to get career advice")
