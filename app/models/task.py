from pydantic import Field, BaseModel
from typing import Optional, Annotated
from bson import ObjectId
from datetime import datetime, timezone
from enum import Enum
from pydantic import BeforeValidator, PlainSerializer

def validate_object_id(v):
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

# Use Annotated with both validator and serializer for Pydantic v2
PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str)
]

class TaskStatus(str, Enum):
  PENDING = "pending"
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"
  CANCELLED = "cancelled"

class TaskModel(BaseModel):
  """Task Document for MongoDB"""
  id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
  title: str = Field(min_length=3, max_length=50)
  status: TaskStatus = Field(default=TaskStatus.PENDING)
  created_by: str
  completed_at: Optional[datetime] = None
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  
  model_config = {
    "populate_by_name": True,
    "arbitrary_types_allowed": True,
    "json_schema_extra": {
      "example": {
        "title": "Read some articles",
        "status": "pending",
        "created_by": "user123",
        "completed_at": None,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      }
    }
  }
