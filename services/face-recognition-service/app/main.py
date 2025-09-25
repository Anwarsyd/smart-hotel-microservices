from fastapi import FastAPI
from app.routes.face_routes import router as face_routes
from app.database.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Face Recognition Service")

# Include routes
app.include_router(face_routes)