from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.face import FaceCreate, FaceVerify, FaceResponse
from app.database.database import get_db
from app.services.face_service import add_face, verify_face, get_all_faces, get_face_by_id, delete_face
from typing import List

router = APIRouter()

@router.post("/add", response_model=FaceResponse)
def add_face_controller(face: FaceCreate, db: Session = Depends(get_db)):
    created_face = add_face(db, face.name, face.embedding)
    return FaceResponse(id=created_face.id, name=created_face.name)

@router.post("/verify", response_model=FaceResponse)
def verify_face_controller(face: FaceVerify, db: Session = Depends(get_db)):
    verified_face = verify_face(db, face.embedding)
    if not verified_face:
        raise HTTPException(status_code=404, detail="Face not recognized")
    return FaceResponse(id=verified_face.id, name=verified_face.name)

@router.get("/", response_model=List[FaceResponse])
def get_all_faces_controller(db: Session = Depends(get_db)):
    faces = get_all_faces(db)
    return [FaceResponse(id=face.id, name=face.name) for face in faces]

@router.get("/{face_id}", response_model=FaceResponse)
def get_face_controller(face_id: int, db: Session = Depends(get_db)):
    face = get_face_by_id(db, face_id)
    if not face:
        raise HTTPException(status_code=404, detail="Face not found")
    return FaceResponse(id=face.id, name=face.name)

@router.delete("/{face_id}")
def delete_face_controller(face_id: int, db: Session = Depends(get_db)):
    deleted_face = delete_face(db, face_id)
    if not deleted_face:
        raise HTTPException(status_code=404, detail="Face not found")
    return {"message": "Face deleted"}