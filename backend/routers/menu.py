from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import json, os


router = APIRouter(prefix="/api/menu", tags=["Menu"])


#file path
MENU_FILE = os.path.join(os.path.dirname(__file__), '..', 'menu.json')
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')


#load config
def _load():
    if not os.path.exists(MENU_FILE):
        return []
    with open(MENU_FILE) as f:
        return json.load(f)

#save data
def _save(data):
    with open(MENU_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def _require_admin(authorization: Optional[str]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    with open(USERS_FILE) as f:
        users = json.load(f)
    user = next((u for u in users if u.get('token') == token), None)
    if not user or user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="Admins only")
    return user


class MenuItemIn(BaseModel):
    name: str
    category: str
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_available: bool = True


@router.get("/")
def get_all():
    return _load()


@router.get("/{item_id}")
def get_one(item_id: int):
    items = _load()
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/")
def create(body: MenuItemIn, authorization: Optional[str] = Header(None)):
    _require_admin(authorization)
    items = _load()
    new_id = (max((i['id'] for i in items), default=0)) + 1
    item = {"id": new_id, **body.dict()}
    items.append(item)
    _save(items)
    return item


@router.put("/{item_id}")
def update(item_id: int, body: MenuItemIn, authorization: Optional[str] = Header(None)):
    _require_admin(authorization)
    items = _load()
    for i, item in enumerate(items):
        if item['id'] == item_id:
            items[i] = {"id": item_id, **body.dict()}
            _save(items)
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")




@router.delete("/{item_id}")
def delete(item_id: int, authorization: Optional[str] = Header(None)):
    _require_admin(authorization)
    items = _load()
    items = [i for i in items if i['id'] != item_id]
    _save(items)
    return {"message": "Deleted"}
