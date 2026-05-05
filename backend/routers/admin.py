from fastapi import APIRouter

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/dashboard")
def dashboard():
    return {
        "total_orders": 0,
        "pending_orders": 0,
        "total_reservations": 0,
        "pending_reservations": 0,
        "total_customers": 0,
        "total_revenue": 0
    }
