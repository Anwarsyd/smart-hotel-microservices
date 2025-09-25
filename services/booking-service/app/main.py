from fastapi import FastAPI
from app.routes.booking_routes import router as booking_routes
from app.database.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking Service")

# Include routes
app.include_router(booking_routes)