from fastapi import FastAPI
from app.routes import hotel_routes

app = FastAPI(title="Hotel Service", version="1.0.0")

app.include_router(hotel_routes.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "hotel-service"}

@app.get("/health")
def health():
    return {"status": "healthy"}
