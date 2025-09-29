from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema


# Custom ObjectId for Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler):
        schema = handler(core_schema.str_schema())
        schema.update(type="string")
        return schema


# Main Notification model
class Notification(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: int
    title: str
    message: str
    type: str = "general"  # email, sms, push, general
    status: str = "pending"  # pending, sent, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None

    class Config:
        populate_by_name = True  # replaces allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
