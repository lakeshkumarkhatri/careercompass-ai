import json
import logging
from google import genai
from config import settings
from models.resume import ResumeAnalysis

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.google_api_key)

def load_prompt(file_path: str) -> str:
    """Load prompt template from file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

async def analyze_resume(resume_text: str) -> ResumeAnalysis:
    """Analyze resume using Gemini."""
    prompt_template = load_prompt("prompts/resume_analysis.txt")
    prompt = prompt_template.format(resume_text=resume_text)
    
    try:
        response = client.models.generate_content(
            model=settings.model_name,
            contents=prompt,
        )
        
        # Parse JSON from response
        # Assuming model returns clean JSON, might need cleanup
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
        
        data = json.loads(response_text)
        return ResumeAnalysis(**data)
        
    except Exception as e:
        logger.error(f"Error analyzing resume with Gemini: {e}")
        raise ValueError("Failed to analyze resume")
