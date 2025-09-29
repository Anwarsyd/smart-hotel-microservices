from app.database.database import get_sync_db
from app.models.notification import Notification
from datetime import datetime
from bson import ObjectId
from typing import List, Optional

def create_notification(user_id: int, title: str, message: str, notification_type: str = "general"):
    db = get_sync_db()
    notification_data = {
        "user_id": user_id,
        "title": title,
        "message": message,
        "type": notification_type,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "sent_at": None
    }
    
    result = db.notifications.insert_one(notification_data)
    notification_data["_id"] = result.inserted_id
    return notification_data

def get_all_notifications() -> List[dict]:
    db = get_sync_db()
    notifications = list(db.notifications.find())
    for notification in notifications:
        notification["id"] = str(notification["_id"])
    return notifications

def get_notification_by_id(notification_id: str) -> Optional[dict]:
    db = get_sync_db()
    if not ObjectId.is_valid(notification_id):
        return None
    
    notification = db.notifications.find_one({"_id": ObjectId(notification_id)})
    if notification:
        notification["id"] = str(notification["_id"])
    return notification

def get_notifications_by_user(user_id: int) -> List[dict]:
    db = get_sync_db()
    notifications = list(db.notifications.find({"user_id": user_id}))
    for notification in notifications:
        notification["id"] = str(notification["_id"])
    return notifications

def update_notification_status(notification_id: str, status: str, sent_at: datetime = None):
    db = get_sync_db()
    if not ObjectId.is_valid(notification_id):
        return None
    
    update_data = {"status": status}
    if sent_at:
        update_data["sent_at"] = sent_at
    
    result = db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": update_data}
    )
    
    if result.matched_count:
        return get_notification_by_id(notification_id)
    return None

def delete_notification(notification_id: str):
    db = get_sync_db()
    if not ObjectId.is_valid(notification_id):
        return None
    
    notification = get_notification_by_id(notification_id)
    if notification:
        db.notifications.delete_one({"_id": ObjectId(notification_id)})
    return notification