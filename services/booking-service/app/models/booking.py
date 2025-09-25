from sqlalchemy import Column, Integer, String, DateTime
from app.database.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    hotel_id = Column(Integer, index=True)
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    status = Column(String, default="confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)