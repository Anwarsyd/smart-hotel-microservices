from fastapi import APIRouter, HTTPException
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from app.services.notification_service import (
    create_notification, 
    get_all_notifications, 
    get_notification_by_id,
    get_notifications_by_user,
    update_notification_status, 
    delete_notification
)
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/", response_model=NotificationResponse)
def create_notification_controller(notification: NotificationCreate):
    created_notification = create_notification(
        notification.user_id, 
        notification.title, 
        notification.message, 
        notification.type
    )
    created_notification["id"] = str(created_notification["_id"])
    return created_notification

@router.get("/", response_model=List[NotificationResponse])
def get_notifications_controller():
    return get_all_notifications()

@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications_controller(user_id: int):
    return get_notifications_by_user(user_id)

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification_controller(notification_id: str):
    notification = get_notification_by_id(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification_controller(notification_id: str, notification: NotificationUpdate):
    sent_at = notification.sent_at if notification.sent_at else datetime.utcnow()
    updated_notification = update_notification_status(notification_id, notification.status, sent_at)
    if not updated_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification

@router.delete("/{notification_id}")
def delete_notification_controller(notification_id: str):
    deleted_notification = delete_notification(notification_id)
    if not deleted_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted"}