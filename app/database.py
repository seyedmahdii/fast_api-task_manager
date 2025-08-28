from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
  client = Optional[AsyncIOMotorClient] = None
  database = None
  
async def connect_to_mongo():
  """Create database connection"""
  try:
    mongo_url = "mongodb://localhost:27017"
    Database.client = AsyncIOMotorClient(mongo_url)
    Database.database = Database.client.task_manager
    
    await Database.client.admin.command('ping')
    logger.info("Connected to MongoDB")
  except ConnectionFailure as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise e
  except Exception as e:
    logger.error(f"Unexpected error connecting to MongoDB: {e}")
    raise
  
async def close_mongo_connection():
  """Close database connection"""
  if Database.client:
    Database.client.close()
    logger.info("Closed MongoDB connection")
    
def get_database():
  """Get the database instance"""
  return Database.database

def get_collection(collection_name: str):
  """Get a collection from the database"""
  return Database.database[collection_name]
