from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.booking import BookingCreate, BookingUpdate
from app.database.database import get_db
from app.services.booking_service import create_booking, get_all_bookings, get_booking_by_id, update_booking_status, delete_booking

router = APIRouter()

@router.post("/")
def create_booking_controller(booking: BookingCreate, db: Session = Depends(get_db)):
    return create_booking(db, booking.user_id, booking.hotel_id, booking.check_in_date, booking.check_out_date)

@router.get("/")
def get_bookings_controller(db: Session = Depends(get_db)):
    return get_all_bookings(db)

@router.get("/{booking_id}")
def get_booking_controller(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}")
def update_booking_controller(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    updated_booking = update_booking_status(db, booking_id, booking.status)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

@router.delete("/{booking_id}")
def delete_booking_controller(booking_id: int, db: Session = Depends(get_db)):
    deleted_booking = delete_booking(db, booking_id)
    if not deleted_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}