from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Verify service status."""
    return {
        "status": "healthy",
        "service": "CareerCompass AI"
    }
