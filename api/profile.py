from fastapi import APIRouter, HTTPException
from models.user_profile import UserProfile
from services.user_profile_service import create_profile, get_profile
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/profile", response_model=UserProfile)
async def create_user_profile(profile: UserProfile):
    """Create or update a user profile."""
    try:
        create_profile(profile)
        return profile
    except Exception as e:
        logger.error(f"Failed to create profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to create profile")

@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """Read a user profile."""
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
