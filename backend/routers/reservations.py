from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])

from routers._auth_helper import get_user_from_token
from services import reservation_service


class ReservationIn(BaseModel):
    date: str
    time: str
    guests: int
    table_number: int


class StatusUpdate(BaseModel):
    status: str


@router.post("/")
def create_reservation(body: ReservationIn, authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    return reservation_service.create_reservation(
        user_id=user['id'],
        date=body.date,
        time=body.time,
        guests=body.guests,
        table_number=body.table_number
    )


@router.get("/me")
def my_reservations(authorization: Optional[str] = Header(None)):
    user = get_user_from_token(authorization)
    return reservation_service.get_reservations_by_user(user['id'])


@router.get("/")
def all_reservations(authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)  # any logged-in user (admin web)
    return reservation_service.get_all_reservations()


@router.put("/{reservation_id}/status")
def update_status(reservation_id: int, body: StatusUpdate, authorization: Optional[str] = Header(None)):
    get_user_from_token(authorization)
    r = reservation_service.update_reservation_status(reservation_id, body.status)
    if not r:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return r
