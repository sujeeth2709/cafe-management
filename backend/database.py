
import json
import os
from datetime import datetime

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _load_users() -> list:
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users: list):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2, default=str)



def get_all_users() -> list:
    return _load_users()


def get_user_by_email(email: str) -> dict | None:
    users = _load_users()
    return next((u for u in users if u["email"] == email), None)


def get_user_by_id(user_id: int) -> dict | None:
    users = _load_users()
    return next((u for u in users if u["id"] == user_id), None)




def create_user(name: str, email: str, hashed_password: str, role: str = "customer") -> dict:
    users = _load_users()
    new_user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "role": role,
        "created_at": datetime.now().isoformat()
    }
    
    users.append(new_user)
    _save_users(users)
    return new_user
