from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from services.resume_service import extract_text_from_pdf
from services.gemini_service import analyze_resume
from services.job_matching_service import get_top_matches
from agents.orchestrator_agent import OrchestratorAgent
from models.career_report import CareerReport
from models.job_match import JobMatchResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/career-report", response_model=CareerReport)
async def career_report_endpoint(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(None)
):
    """Analyze resume, match jobs, and provide unified career report."""
    logger.info(f"Received career report request for file: {file.filename}, user_id: {user_id}")
    
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
        
    # 4. Orchestrate
    try:
        orchestrator = OrchestratorAgent()
        report = await orchestrator.get_report(analysis, match_response, user_id=user_id)
        return report
    except Exception as e:
        logger.error(f"Career report generation failed: {e}")
        raise HTTPException(status_code=500, detail="Career report generation failed")
