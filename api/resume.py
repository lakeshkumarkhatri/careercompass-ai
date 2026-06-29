from fastapi import APIRouter, UploadFile, File, HTTPException
from services.resume_service import extract_text_from_pdf
from services.gemini_service import analyze_resume
from models.resume import ResumeAnalysis
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze-resume", response_model=ResumeAnalysis)
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    """Analyze an uploaded resume PDF."""
    logger.info(f"Received resume analysis request for file: {file.filename}")
    
    text = await extract_text_from_pdf(file)
    
    try:
        analysis = await analyze_resume(text)
        return analysis
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Resume analysis failed")
