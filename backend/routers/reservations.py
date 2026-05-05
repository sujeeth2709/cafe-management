from fastapi import APIRouter

router = APIRouter(prefix="/api/reservations", tags=["Reservations"])

@router.get("/")
def all_reservations():
    return []

@router.post("/")
def create_reservation(reservation: dict):
    return {"message": "Reservation created", "reservation": reservation}
