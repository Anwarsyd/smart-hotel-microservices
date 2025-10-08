from pydantic import BaseModel
from typing import Optional, List

class HotelBase(BaseModel):
    name: str
    city: str
    address: str
    rating: Optional[float] = 0.0
    description: Optional[str]

class HotelCreate(HotelBase):
    pass

class HotelUpdate(HotelBase):
    pass

class HotelResponse(HotelBase):
    id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price: float
    availability: Optional[int] = 1

class RoomResponse(RoomBase):
    id: int
    hotel_id: int

    class Config:
        from_attributes = True
