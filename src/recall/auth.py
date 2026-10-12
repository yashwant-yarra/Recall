from fastapi import HTTPException
from .config import settings

def get_current_user_id() -> str:
    """
    Get the current user ID from the environment variable.
    Raises an HTTPException if the user ID is not set.
    """
    if settings.dev_user_id is None:
        raise HTTPException(status_code=500, detail="DEV_USER_ID is not set in the environment.")
    return settings.dev_user_id