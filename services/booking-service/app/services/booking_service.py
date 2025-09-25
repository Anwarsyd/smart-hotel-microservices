from sqlalchemy.orm import Session
from app.models.booking import Booking
from datetime import datetime

def create_booking(db: Session, user_id: int, hotel_id: int, check_in_date: datetime, check_out_date: datetime):
    booking = Booking(user_id=user_id, hotel_id=hotel_id, check_in_date=check_in_date, check_out_date=check_out_date)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def get_all_bookings(db: Session):
    return db.query(Booking).all()

def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def update_booking_status(db: Session, booking_id: int, status: str):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        booking.status = status
        db.commit()
        db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
    return booking