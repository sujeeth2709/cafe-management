from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime


class ReservationCreate(BaseModel):
    date: date
    time: time
    guests: int


class ReservationOut(BaseModel):
    id: int
    user_id: int
    date: date
    time: time
    guests: int
    status: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class ReservationStatusUpdate(BaseModel):
    status: str