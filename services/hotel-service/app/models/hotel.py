from sqlalchemy import Column, Integer, String, Float, Text
from app.database.database import Base

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    rating = Column(Float, default=0.0)
    description = Column(Text, nullable=True)
