from sqlalchemy.orm import Session
from models.reservation import Reservation
from schemas.reservation import ReservationCreate


def create_reservation(db: Session, reservation: ReservationCreate, user_id: int):
    new_reservation = Reservation(user_id=user_id, **reservation.model_dump())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation


def get_reservations_by_user(db: Session, user_id: int):
    return db.query(Reservation).filter(Reservation.user_id == user_id).all()


def get_all_reservations(db: Session):
    return db.query(Reservation).all()


def update_reservation_status(db: Session, reservation_id: int, status: str):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        return None
    reservation.status = status
    db.commit()
    db.refresh(reservation)
    return reservation
