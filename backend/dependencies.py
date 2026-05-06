from fastapi import Header, HTTPException
from routers._auth_helper import get_user_from_token, require_admin as _require_admin


def get_current_user(authorization: str | None = Header(default=None)):
    """FastAPI dependency — returns current user dict from JSON store."""
    return get_user_from_token(authorization)


def require_admin(authorization: str | None = Header(default=None)):
    """FastAPI dependency — returns user only if role == 'admin'."""
    return _require_admin(authorization)
