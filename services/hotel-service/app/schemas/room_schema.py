from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price_per_night: float
    is_available: Optional[bool] = True

class RoomCreate(RoomBase):
    hotel_id: int

class RoomResponse(RoomBase):
    id: int
    hotel_id: int
    class Config:
        from_attributes = True
