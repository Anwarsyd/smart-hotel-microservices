from fastapi import APIRouter
from app.controllers.face_controller import router as face_router

router = APIRouter()
router.include_router(face_router, prefix="/faces", tags=["Faces"])