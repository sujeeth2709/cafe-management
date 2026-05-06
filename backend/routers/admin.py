from fastapi import APIRouter, Header
from typing import Optional
import json, os

router = APIRouter(prefix="/api/admin", tags=["Admin"])

from routers._auth_helper import get_user_from_token
from services import order_service, reservation_service

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')


@router.get("/dashboard")
def dashboard(authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)  # just needs valid login

    orders = order_service.get_all_orders()
    reservations = reservation_service.get_all_reservations()

    total_revenue = sum(o['total_price'] for o in orders if o['status'] == 'delivered')
    pending_orders = sum(1 for o in orders if o['status'] == 'pending')
    pending_reservations = sum(1 for r in reservations if r['status'] == 'pending')

    customers = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            customers = json.load(f)

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": len(orders),
        "pending_orders": pending_orders,
        "total_reservations": len(reservations),
        "pending_reservations": pending_reservations,
        "total_customers": len(customers),
    }


@router.get("/cashflow")
def cashflow(authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    return order_service.get_daily_summary()
