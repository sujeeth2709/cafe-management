from pydantic import BaseModel
from typing import Optional


class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_available: Optional[bool] = True
    image_url: Optional[str] = None


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


class MenuItemOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    is_available: bool
    image_url: Optional[str]

    class Config:
        from_attributes = True