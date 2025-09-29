from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/notification_service")

# Async MongoDB client for FastAPI
async_client = AsyncIOMotorClient(MONGO_URI)
async_db = async_client.get_database()

# Sync MongoDB client for non-async operations
sync_client = MongoClient(MONGO_URI)
sync_db = sync_client.get_database()

# Get async database
async def get_async_db():
    return async_db

# Get sync database  
def get_sync_db():
    return sync_db