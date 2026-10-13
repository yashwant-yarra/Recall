from fastapi import HTTPException

from .config import settings


# Placeholder until real auth; DEV_USER_ID is unset in prod, so this fails closed.
def get_current_user_id() -> str:
    if settings.dev_user_id is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return settings.dev_user_id
