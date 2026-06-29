from fastapi import APIRouter, UploadFile, File, HTTPException
from services.resume_service import extract_text_from_pdf
from services.gemini_service import analyze_resume
from services.job_matching_service import get_top_matches
from agents.career_advisor_agent import get_career_advice
from agents.interview_coach_agent import InterviewCoachAgent
from models.interview_coach import InterviewCoach
from models.job_match import JobMatchResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/interview-coach", response_model=InterviewCoach)
async def interview_coach_endpoint(file: UploadFile = File(...)):
    """Analyze resume, match jobs, get advice, and provide interview coaching."""
    logger.info(f"Received interview coaching request for file: {file.filename}")
    
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
    except Exception as e:
        logger.error(f"Career advice generation failed: {e}")
        raise HTTPException(status_code=500, detail="Career advice generation failed")
        
    # 5. Get Interview Coaching
    try:
        coach_agent = InterviewCoachAgent()
        coaching = await coach_agent.get_coaching(analysis, match_response, advice)
        return coaching
    except Exception as e:
        logger.error(f"Interview coaching generation failed: {e}")
        raise HTTPException(status_code=500, detail="Interview coaching generation failed")
