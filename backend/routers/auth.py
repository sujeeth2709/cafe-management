from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserLogin, UserOut, Token
from utils.helpers import hash_password, verify_password
from services.auth_service import create_access_token
import database

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    existing = database.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = database.create_user(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="customer"
    )
    return new_user


@router.post("/login", response_model=Token)
def login(user: UserLogin):
    db_user = database.get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": str(db_user["id"])})
    return {"access_token": token, "token_type": "bearer"}
