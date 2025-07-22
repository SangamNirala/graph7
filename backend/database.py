from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from config import MONGO_URL, DATABASE_NAME

class DatabaseManager:
    client: Optional[AsyncIOMotorClient] = None
    database = None

db_manager = DatabaseManager()

async def connect_to_mongo():
    """Create database connection."""
    db_manager.client = AsyncIOMotorClient(MONGO_URL)
    db_manager.database = db_manager.client[DATABASE_NAME]
    print(f"Connected to MongoDB at {MONGO_URL}")

async def close_mongo_connection():
    """Close database connection."""
    if db_manager.client:
        db_manager.client.close()
        print("Disconnected from MongoDB")

def get_database():
    """Get database instance."""
    return db_manager.database