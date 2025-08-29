from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId): 
  """Custom ObjectId for MongoDB compatibility"""
  @classmethod
  def __get_validators__(cls):
    yield cls.validate
    
  @classmethod
  def validate(cls, v):
    if not ObjectId.is_valid(v):
      raise ValueError("Invalid ObjectId")
    return ObjectId(v)
  
  @classmethod
  def __modify_schema__(cls, field_schema):
    field_schema.update(type="string")
  
class UserModel(BaseModel):
  """User document model for MongoDB"""
  id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
  email: EmailStr = Field(unique=True, index=True)
  username: str = Field(min_length=3, max_length=50)
  full_name: str = Field(min_length=3, max_length=50)
  hashed_password: str
  is_active: bool = Field(default=True)
  is_superuser: bool = Field(default=False)
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow)
  
  class Config:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    schema_extra = {
      "example": {
        "email": "user@example.com",
        "username": "user123",
        "full_name": "John Doe",
        "is_active": True,
        "is_superuser": False,
      }
    }