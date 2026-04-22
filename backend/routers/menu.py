from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.menu import MenuItemCreate, MenuItemUpdate, MenuItemOut
from services import menu_service
from dependencies import require_admin

router = APIRouter(prefix="/api/menu", tags=["Menu"])


@router.get("/", response_model=List[MenuItemOut])
def get_all(db: Session = Depends(get_db)):
    return menu_service.get_all_items(db)


@router.get("/{item_id}", response_model=MenuItemOut)
def get_one(item_id: int, db: Session = Depends(get_db)):
    item = menu_service.get_item_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=MenuItemOut)
def create(item: MenuItemCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    return menu_service.create_item(db, item)


@router.put("/{item_id}", response_model=MenuItemOut)
def update(item_id: int, item: MenuItemUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    updated = menu_service.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    deleted = menu_service.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}