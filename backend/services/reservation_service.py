import json
import os
from datetime import datetime

RESERVATIONS_FILE = os.path.join(os.path.dirname(__file__), '..', 'reservations.json')


def _load():
    if not os.path.exists(RESERVATIONS_FILE):
        return []
    with open(RESERVATIONS_FILE, 'r') as f:
        return json.load(f)


def _save(data):
    with open(RESERVATIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def create_reservation(user_id: int, date: str, time: str, guests: int, table_number: int):
    reservations = _load()
    new_id = (max((r['id'] for r in reservations), default=0)) + 1
    reservation = {
        "id": new_id,
        "user_id": user_id,
        "table_number": table_number,
        "date": str(date),
        "time": str(time),
        "guests": guests,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    reservations.append(reservation)
    _save(reservations)
    return reservation


def get_reservations_by_user(user_id: int):
    return [r for r in _load() if r['user_id'] == user_id]


def get_all_reservations():
    return _load()


def update_reservation_status(reservation_id: int, status: str):
    reservations = _load()
    for r in reservations:
        if r['id'] == reservation_id:
            r['status'] = status
            _save(reservations)
            return r
    return None
