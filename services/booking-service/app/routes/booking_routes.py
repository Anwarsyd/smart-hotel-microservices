from fastapi import APIRouter
from app.controllers.booking_controller import router as booking_router

router = APIRouter()
router.include_router(booking_router, prefix="/bookings", tags=["Bookings"])