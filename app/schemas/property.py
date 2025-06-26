from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal
from enum import Enum


class PropertyType(str, Enum):
    apartment = "apartment"
    house = "house"
    vacation = "vacation"


class PropertyCreate(BaseModel):
    city: str
    address: str
    price: Decimal
    yield_percent: Optional[Decimal] = None
    property_type: Optional[PropertyType] = None
    rooms: Optional[int] = None
    floor: Optional[int] = None
    description: Optional[str] = None
    rental_estimate: Optional[Decimal] = None


class PropertyUpdate(BaseModel):
    city: Optional[str] = None
    address: Optional[str] = None
    price: Optional[Decimal] = None
    yield_percent: Optional[Decimal] = None
    property_type: Optional[PropertyType] = None
    rooms: Optional[int] = None
    floor: Optional[int] = None
    description: Optional[str] = None
    rental_estimate: Optional[Decimal] = None


class PropertyOut(PropertyCreate):
    id: UUID
    image_url: Optional[str] = None


class PublicPropertyOut(BaseModel):
    id: str
    city: str
    address: str
    price: float
    rooms: int | None = None
    floor: int | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True
