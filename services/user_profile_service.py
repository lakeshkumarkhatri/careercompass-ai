import json
import logging
from pathlib import Path
from typing import Optional, Dict
from models.user_profile import UserProfile

logger = logging.getLogger(__name__)

DATA_PATH = Path("data/users.json")

def _load_all_users() -> Dict[str, UserProfile]:
    """Load all users from JSON file."""
    if not DATA_PATH.exists():
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {uid: UserProfile(**user) for uid, user in data.items()}
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Failed to load users: {e}")
        return {}

def _save_all_users(users: Dict[str, UserProfile]) -> None:
    """Save all users to JSON file."""
    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump({uid: user.model_dump() for uid, user in users.items()}, f, indent=4)

def create_profile(profile: UserProfile) -> None:
    """Create or update a user profile."""
    users = _load_all_users()
    users[profile.user_id] = profile
    _save_all_users(users)
    logger.info(f"Profile created/updated for user: {profile.user_id}")

def get_profile(user_id: str) -> Optional[UserProfile]:
    """Read a user profile."""
    users = _load_all_users()
    return users.get(user_id)
