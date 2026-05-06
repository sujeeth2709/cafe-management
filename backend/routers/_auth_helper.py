import json, os
from fastapi import HTTPException

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')


def get_user_from_token(authorization: str | None):
    """Return user dict if token is valid. Raises 401 if not."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    if not os.path.exists(USERS_FILE):
        raise HTTPException(status_code=401, detail="No users found")
    with open(USERS_FILE) as f:
        users = json.load(f)
    user = next((u for u in users if u.get('token') == token), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token — please log out and log in again")
    return user


def require_admin(authorization: str | None):
    """Same as above but also checks admin role."""
    user = get_user_from_token(authorization)
    if user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    return user
