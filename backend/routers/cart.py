from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.menu import MenuItem
from schemas.menu import MenuItemOut

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.post("/validate")
def validate_cart(item_ids: List[int], db: Session = Depends(get_db)):
    """
    Validates that all items in the cart exist and are available.
    Frontend sends list of menu item IDs before placing order.
    """
    invalid = []
    for item_id in item_ids:
        item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not item or not item.is_available:
            invalid.append(item_id)

    if invalid:
        raise HTTPException(
            status_code=400,
            detail=f"These items are unavailable or do not exist: {invalid}"
        )

    return {"message": "All items are valid and available"}
