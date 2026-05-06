from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json, os, hashlib, secrets

router = APIRouter(prefix="/api/auth", tags=["Auth"])

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')


def _load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE) as f:
        return json.load(f)


def _save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def _sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _verify_password(plain: str, stored_hash: str) -> bool:
    # Try SHA256 first (new users)
    if stored_hash == _sha256(plain):
        return True
    # Try bcrypt (existing users from old SQLAlchemy system)
    try:
        import bcrypt
        return bcrypt.checkpw(plain.encode(), stored_hash.encode())
    except Exception:
        return False


class RegisterIn(BaseModel):
    name: str
    email: str
    password: str


class LoginIn(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(body: RegisterIn):
    users = _load_users()
    if any(u['email'] == body.email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")
    new_id = (max((u['id'] for u in users), default=0)) + 1
    role = "admin" if not users else "customer"
    user = {
        "id": new_id,
        "name": body.name,
        "email": body.email,
        "hashed_password": _sha256(body.password),
        "role": role,
        "token": None,
        "created_at": __import__('datetime').datetime.now().isoformat()
    }
    users.append(user)
    _save_users(users)
    return {"message": "Registered successfully", "role": role}


@router.post("/login")
def login(body: LoginIn):
    users = _load_users()
    user = next((u for u in users if u['email'] == body.email), None)
    if not user or not _verify_password(body.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = secrets.token_hex(32)
    user['token'] = token
    if 'role' not in user:
        user['role'] = 'customer'
    _save_users(users)

    return {
        "token": token,
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "role": user['role']
        }
    }
