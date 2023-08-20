import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.config import mongo_config

client = AsyncIOMotorClient(mongo_config.mongo_url)


def init_db() -> AsyncIOMotorDatabase:
    db = client[mongo_config.db_name]
    return db
