import fitz  # PyMuPDF
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

async def extract_text_from_pdf(file: UploadFile) -> str:
    """Extract text content from a PDF file."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract text from PDF")
