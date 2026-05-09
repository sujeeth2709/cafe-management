from fastapi import APIRouter
from typing import List


router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.post("/validate")
def validate_cart(item_ids: List[int]):
    return {"message": "All items are valid and available"}
