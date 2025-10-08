from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_number = Column(String, nullable=False)
    room_type = Column(String, nullable=False)  # e.g., single, double, suite
    price = Column(Float, nullable=False)
    availability = Column(Integer, default=1)  # 1 = available, 0 = booked

    hotel = relationship("Hotel", backref="rooms")
