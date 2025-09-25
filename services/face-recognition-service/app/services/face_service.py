from sqlalchemy.orm import Session
from app.models.face import Face

def add_face(db: Session, name: str, embedding: bytes):
    face = Face(name=name, embedding=embedding)
    db.add(face)
    db.commit()
    db.refresh(face)
    return face

def get_all_faces(db: Session):
    return db.query(Face).all()

def get_face_by_id(db: Session, face_id: int):
    return db.query(Face).filter(Face.id == face_id).first()

def verify_face(db: Session, embedding: bytes):
    faces = db.query(Face).all()
    for face in faces:
        if face.embedding == embedding:  # simple equality; replace with cosine distance for real case
            return face
    return None

def delete_face(db: Session, face_id: int):
    face = db.query(Face).filter(Face.id == face_id).first()
    if face:
        db.delete(face)
        db.commit()
    return face