from fastapi import APIRouter, UploadFile, File, HTTPException
from services.resume_service import extract_text_from_pdf
from services.gemini_service import analyze_resume
from services.job_matching_service import get_top_matches
from agents.career_advisor_agent import get_career_advice
from models.career_advice import CareerAdvice
from models.job_match import JobMatchResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/career-advice", response_model=CareerAdvice)
async def career_advice_endpoint(file: UploadFile = File(...)):
    """Analyze resume, match jobs, and provide career advice."""
    logger.info(f"Received career advice request for file: {file.filename}")
    
    # 1. Extract text
    text = await extract_text_from_pdf(file)
    
    # 2. Analyze resume (get skills/info)
    try:
        analysis = await analyze_resume(text)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Resume analysis failed")
    
    if not analysis.skills:
        raise HTTPException(status_code=400, detail="No skills found in uploaded resume.")
        
    # 3. Match jobs
    try:
        matches = get_top_matches(analysis.skills)
        match_response = JobMatchResponse(
            candidate_name=analysis.candidate_name,
            matches=matches
        )
    except Exception as e:
        logger.error(f"Job matching failed: {e}")
        raise HTTPException(status_code=500, detail="Job matching failed")
        
    # 4. Get Career Advice
    try:
        advice = await get_career_advice(analysis, match_response)
        return advice
    except Exception as e:
        logger.error(f"Career advice generation failed: {e}")
        raise HTTPException(status_code=500, detail="Career advice generation failed")
