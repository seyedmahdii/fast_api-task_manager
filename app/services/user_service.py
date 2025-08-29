from app.database import get_collection
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.auth.password import hash_password, verify_password
from bson import ObjectId
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class UserService:
  def __init__(self):
    self.collection = get_collection("users")
    
  async def create_user(self, user_data: UserCreate) -> UserResponse:
    """Create a new user"""
    try:
      # Check if email already exists
      existing_user = await self.collection.find_one({"email": user_data.email})
      if existing_user:
        raise ValueError("Email already exists")
      
      # Check if username already exists
      existing_user = await self.collection.find_one({"username": user_data.username})
      if existing_user:
        raise ValueError("Username already exists")
      
      # Hash password
      hashed_password = hash_password(user_data.password)
      
      user_doc = {
        "email": user_data.email,
        "username": user_data.username,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_superuser": False
      }
      
      result = await self.collection.insert_one(user_doc)
      
      created_user = await self.collection.find_one({"_id": result.inserted_id})
      
      # Convert to UserResponse schema
      return UserResponse(
        id=str(created_user["_id"]),
        email=created_user["email"],
        username=created_user["username"],
        full_name=created_user["full_name"],
        is_active=created_user["is_active"],
        is_superuser=created_user["is_superuser"],
        created_at=created_user["created_at"],
        updated_at=created_user["updated_at"]
      )
    except Exception as e:
      logger.error(f"Error creating user: {e}")
      raise
  
  async def get_user_by_email(self, email: str) -> Optional[UserModel]:
    """Get user by email"""
    try:
      user_doc = await self.collection.find_one({"email": email})
      if user_doc:
        return UserModel(**user_doc)
    except Exception as e:
      logger.error(f"Error getting user by email: {e}")
      raise
  
  async def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
    """Get user by ID"""
    try:
      user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
      if user_doc:
          return UserModel(**user_doc)
      return None
    except Exception as e:
      logger.error(f"Error getting user by ID: {e}")
      raise
    
  async def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
    """Authenticate user with email and password"""
    try:
      user_doc = await self.get_user_by_email(email)
      if not user_doc:
        return None
    
      if not verify_password(password, user_doc.hashed_password):
        return None
      
      return user_doc
    except Exception as e:
      logger.error(f"Error authenticating user: {e}")
      raise
    
  async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserResponse]:
    """Update user"""
    try:
      update_data = {}
      
      if user_data.email is not None:
        update_data["email"] = user_data.email
      if user_data.username is not None:
        update_data["username"] = user_data.username
      if user_data.full_name is not None:
        update_data["full_name"] = user_data.full_name
      if user_data.password is not None:
        hashed_password = hash_password(user_data.password)
        update_data["hashed_password"] = hashed_password
        
      result = await self.collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set", update_data}
      )
      if result.modified_count > 0:
        return await self.get_user_by_id(user_id)
      return None
    except Exception as e:
      logger.error(f"Error updating user: {e}")
      raise
    
  async def delete_user(self, user_id: str) -> bool:
    """Delete user"""
    try:
      result = await self.collection.delete_one({"_id": ObjectId(user_id)})
      return result.deleted_count > 0
    except Exception as e:
      logger.error(f"Error deleting user: {e}")
      raise
    
  async def get_all_users(self, skip: int = 0, limit: int = 10) -> List[UserResponse]:
    """Get all users with pagination"""
    try:
      users = []
      cursor = self.collection.find().skip(skip).limit(limit)
      
      async for user_doc in cursor:
        users.append(UserResponse(
          id=str(user_doc["_id"]),
          email=user_doc["email"],
          username=user_doc["username"],
          full_name=user_doc["full_name"],
          is_active=user_doc["is_active"],
          is_superuser=user_doc["is_superuser"],
          created_at=user_doc["created_at"],
          updated_at=user_doc["updated_at"]
        ))
      
      return users
    except Exception as e:
      logger.error(f"Error getting all users: {e}")
      raise
