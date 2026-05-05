from fastapi import APIRouter

router = APIRouter(prefix="/api/menu", tags=["Menu"])

MENU_ITEMS = [
    {"id": 1, "name": "Espresso", "price": 3.5, "category": "drinks", "is_available": True},
    {"id": 2, "name": "Cappuccino", "price": 4.5, "category": "drinks", "is_available": True},
    {"id": 3, "name": "Croissant", "price": 2.5, "category": "food", "is_available": True},
    {"id": 4, "name": "Club Sandwich", "price": 7.0, "category": "food", "is_available": True},
]

@router.get("/")
def get_all():
    return MENU_ITEMS

@router.get("/{item_id}")
def get_one(item_id: int):
    item = next((i for i in MENU_ITEMS if i["id"] == item_id), None)
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    return item
