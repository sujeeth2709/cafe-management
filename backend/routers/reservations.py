from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.reservation import ReservationCreate, ReservationOut, ReservationStatusUpdate
from services import reservation_service
from dependencies import get_current_user, require_admin
from models.user import User

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationOut)
def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reservation_service.create_reservation(db, reservation, current_user.id)


@router.get("/me", response_model=List[ReservationOut])
def my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reservation_service.get_reservations_by_user(db, current_user.id)


@router.get("/", response_model=List[ReservationOut])
def all_reservations(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return reservation_service.get_all_reservations(db)


@router.put("/{reservation_id}/status", response_model=ReservationOut)
def update_status(
    reservation_id: int,
    body: ReservationStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    updated = reservation_service.update_reservation_status(db, reservation_id, body.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return updated
