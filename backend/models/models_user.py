# models/user.py — plain class, no SQLAlchemy needed
from dataclasses import dataclass

from typing import Optional


@dataclass

class User:
    id: int
    name: str
    email: str
    hashed_password: str
    role: str = "admin"  # Every user is admin
    created_at: Optional[str] = None
