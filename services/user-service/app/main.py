from fastapi import FastAPI
from app.database.database import engine, Base
from app.routes import auth_routes

# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service with Auth", version="1.0.0")

app.include_router(auth_routes.router)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "user-service",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}