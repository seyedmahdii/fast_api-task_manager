from pydantic import Field, BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime
from enum import Enum

class PyObjectId(ObjectId): 
  """Custom ObjectId for MongoDB compatibility"""
  @classmethod
  def __get_validators__(cls):
    yield cls.validate
    
  @classmethod
  def validate(cls, v, handler):
    if not ObjectId.is_valid(v):
      raise ValueError("Invalid ObjectId")
    return ObjectId(v)
  
  @classmethod
  def __get_pydantic_json_schema__(cls, field_schema):
    field_schema.update(type="string")

class TaskStatus(str, Enum):
  PENDING = "pending"
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"
  CANCELLED = "cancelled"

class TaskModel(BaseModel):
  """Task Document for MongoDB"""
  id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
  title: str = Field(min_length=3, max_length=50)
  status: TaskStatus = Field(default=TaskStatus.PENDING)
  created_by: str
  completed_at: Optional[datetime] = None
  created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
  
  class Config:
    validate_by_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    json_schema_extra = {
      "example": {
        "title": "Read some articles",
        "status": "pending",
        "created_by": "user123",
        "completed_at": None,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      }
    }
