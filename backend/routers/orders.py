from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api/orders", tags=["Orders"])

from routers._auth_helper import get_user_from_token
from services import order_service


class OrderItemIn(BaseModel):
    menu_item_id: int
    name: str
    quantity: int
    price: float


class OrderIn(BaseModel):
    items: List[OrderItemIn]
    table_number: int


class StatusUpdate(BaseModel):
    status: str


@router.post("/")
def create_order(body: OrderIn, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    items = [i.dict() for i in body.items]
    return order_service.create_order(
        user_id=user['id'],
        items=items,
        table_number=body.table_number
    )


@router.get("/me")
def my_orders(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    return order_service.get_orders_by_user(user['id'])


@router.get("/")
def all_orders(authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)  # any logged-in user (admin web)
    return order_service.get_all_orders()


@router.put("/{order_id}/status")
def update_status(order_id: int, body: StatusUpdate, authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    order = order_service.update_order_status(order_id, body.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
