import json
import os
from datetime import datetime

ORDERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'orders.json')


def _load():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, 'r') as f:
        return json.load(f)


def _save(data):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def create_order(user_id: int, items: list, table_number: int):
    orders = _load()
    new_id = (max((o['id'] for o in orders), default=0)) + 1
    total = sum(i['price'] * i['quantity'] for i in items)
    order = {
        "id": new_id,
        "user_id": user_id,
        "table_number": table_number,
        "items": items,
        "total_price": round(total, 2),
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    orders.append(order)
    _save(orders)
    return order


def get_orders_by_user(user_id: int):
    return [o for o in _load() if o['user_id'] == user_id]


def get_all_orders():
    return _load()


def update_order_status(order_id: int, status: str):
    orders = _load()
    for o in orders:
        if o['id'] == order_id:
            o['status'] = status
            _save(orders)
            return o
    return None


def get_daily_summary():
    orders = _load()
    today = datetime.now().date().isoformat()
    summary = {}
    for o in orders:
        day = o['created_at'][:10]
        if day not in summary:
            summary[day] = {"date": day, "order_count": 0, "revenue": 0.0}
        summary[day]["order_count"] += 1
        if o['status'] == 'delivered':
            summary[day]["revenue"] += o['total_price']
    return sorted(summary.values(), key=lambda x: x['date'], reverse=True)
