from fastapi import FastAPI
from app.routes.notification_routes import router as notification_routes

app = FastAPI(title="Notification Service")

# Include routes
app.include_router(notification_routes)

@app.on_event("startup")
async def startup_event():
    # Create indexes for better performance
    from app.database.database import get_sync_db
    db = get_sync_db()
    db.notifications.create_index("user_id")
    db.notifications.create_index("status")
    db.notifications.create_index("created_at")