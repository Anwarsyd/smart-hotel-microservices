from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: str = "general"

class NotificationUpdate(BaseModel):
    status: str
    sent_at: Optional[datetime] = None

class NotificationResponse(BaseModel):
    id: str
    user_id: int
    title: str
    message: str
    type: str
    status: str
    created_at: datetime
    sent_at: Optional[datetime] = None