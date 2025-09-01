from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId
# Import PyObjectId from task.py to avoid duplication
from app.models.task import PyObjectId
  
class UserModel(BaseModel):
  """User document model for MongoDB"""
  id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
  email: EmailStr = Field(unique=True, index=True)
  username: str = Field(min_length=3, max_length=50)
  full_name: str = Field(min_length=3, max_length=50)
  hashed_password: str
  is_active: bool = Field(default=True)
  is_superuser: bool = Field(default=False)
  created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
  
  model_config = {
    "populate_by_name": True,
    "arbitrary_types_allowed": True,
    "json_schema_extra": {
      "example": {
        "email": "user@example.com",
        "username": "user123",
        "full_name": "John Doe",
        "is_active": True,
        "is_superuser": False,
      }
    }
  }