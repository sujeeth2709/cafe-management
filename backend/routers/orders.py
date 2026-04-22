from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from services import order_service
from dependencies import get_current_user, require_admin
from models.user import User

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", response_model=OrderOut)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.create_order(db, order, current_user.id)


@router.get("/me", response_model=List[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return order_service.get_orders_by_user(db, current_user.id)


@router.get("/", response_model=List[OrderOut])
def all_orders(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return order_service.get_all_orders(db)


@router.put("/{order_id}/status", response_model=OrderOut)
def update_status(
    order_id: int,
    body: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    updated = order_service.update_order_status(db, order_id, body.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated
