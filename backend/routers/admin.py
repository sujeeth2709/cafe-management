from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.order import Order
from models.reservation import Reservation
from models.user import User
from dependencies import require_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), admin=Depends(require_admin)):
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    total_reservations = db.query(Reservation).count()
    pending_reservations = db.query(Reservation).filter(Reservation.status == "pending").count()
    total_users = db.query(User).filter(User.role == "customer").count()

    total_revenue = db.query(Order).filter(Order.status == "delivered").all()
    revenue = sum(o.total_price for o in total_revenue)

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_reservations": total_reservations,
        "pending_reservations": pending_reservations,
        "total_customers": total_users,
        "total_revenue": revenue
    }
