from fastapi import APIRouter

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/")
def all_orders():
    return []

@router.post("/")
def create_order(order: dict):
    return {"message": "Order placed", "order": order}
