from pydantic import BaseModel
from datetime import datetime

class BookingCreate(BaseModel):
    user_id: int
    hotel_id: int
    check_in_date: datetime
    check_out_date: datetime

class BookingUpdate(BaseModel):
    status: str