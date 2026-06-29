from fastapi import APIRouter, UploadFile, File, HTTPException
from services.resume_service import extract_text_from_pdf
from services.gemini_service import analyze_resume
from services.job_matching_service import get_top_matches
from models.job_match import JobMatchResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/match-jobs", response_model=JobMatchResponse)
async def match_jobs_endpoint(file: UploadFile = File(...)):
    """Analyze resume and match with top jobs."""
    logger.info(f"Received job matching request for file: {file.filename}")
    
    # 1. Extract text
    text = await extract_text_from_pdf(file)
    
    # 2. Analyze resume (get skills)
    try:
        analysis = await analyze_resume(text)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Resume analysis failed")
    
    # 3. Validation
    if not analysis.skills:
        raise HTTPException(status_code=400, detail="No skills found in uploaded resume.")
        
    # 4. Match jobs
    try:
        matches = get_top_matches(analysis.skills)
        return JobMatchResponse(
            candidate_name=analysis.candidate_name,
            matches=matches
        )
    except Exception as e:
        logger.error(f"Job matching failed: {e}")
        raise HTTPException(status_code=500, detail="Job matching failed")
