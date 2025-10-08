from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.hotel_schema import HotelCreate, HotelUpdate, HotelResponse
from app.services.hotel_service import create_hotel, get_hotel, get_hotels, update_hotel, delete_hotel

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.post("/", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
def create_new_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    return create_hotel(db, hotel)

@router.get("/", response_model=list[HotelResponse])
def list_hotels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_hotels(db, skip, limit)

@router.get("/{hotel_id}", response_model=HotelResponse)
def get_single_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = get_hotel(db, hotel_id)
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel

@router.put("/{hotel_id}", response_model=HotelResponse)
def update_existing_hotel(hotel_id: int, hotel: HotelUpdate, db: Session = Depends(get_db)):
    db_hotel = update_hotel(db, hotel_id, hotel)
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel

@router.delete("/{hotel_id}", response_model=HotelResponse)
def delete_existing_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = delete_hotel(db, hotel_id)
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel
