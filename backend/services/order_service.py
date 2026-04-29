from sqlalchemy.orm import Session
from models.order import Order, OrderItem
from models.menu import MenuItem
from schemas.order import OrderCreate
from fastapi import HTTPException




def create_order(db: Session, order: OrderCreate, user_id: int):
    total = 0
    order_items = []

    for item in order.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
        if not menu_item.is_available:
            raise HTTPException(status_code=400, detail=f"{menu_item.name} is not available")
        item_total = menu_item.price * item.quantity
        total += item_total
        order_items.append({"menu_item_id": item.menu_item_id, "quantity": item.quantity, "price": menu_item.price})

    new_order = Order(user_id=user_id, total_price=total)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for oi in order_items:
        db.add(OrderItem(order_id=new_order.id, **oi))
    db.commit()
    db.refresh(new_order)
    return new_order


def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_all_orders(db: Session):
    return db.query(Order).all()


def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order
