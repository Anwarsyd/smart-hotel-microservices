from fastapi import APIRouter
from app.controllers.notification_controller import router as notification_router

router = APIRouter()
router.include_router(notification_router, prefix="/notifications", tags=["Notifications"])