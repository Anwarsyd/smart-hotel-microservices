from sqlalchemy.orm import Session
from app.models.hotel import Hotel
from app.schemas.hotel_schema import HotelCreate, HotelUpdate

def create_hotel(db: Session, hotel: HotelCreate):
    db_hotel = Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotel(db: Session, hotel_id: int):
    return db.query(Hotel).filter(Hotel.id == hotel_id).first()

def get_hotels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Hotel).offset(skip).limit(limit).all()

def update_hotel(db: Session, hotel_id: int, hotel: HotelUpdate):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_hotel:
        return None
    for key, value in hotel.dict().items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def delete_hotel(db: Session, hotel_id: int):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_hotel:
        return None
    db.delete(db_hotel)
    db.commit()
    return db_hotel
