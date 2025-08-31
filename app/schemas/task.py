from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.task import TaskStatus

class TaskBase(BaseModel):
  title: str = Field(min_length=3, max_length=50)
  
class TaskCreate(TaskBase):
  pass

class TaskUpdate(TaskBase):
  status: TaskStatus = Field(default=TaskStatus.PENDING)
  completed_at: Optional[datetime] = None

class TaskResponse(TaskBase):
  id: str
  status: TaskStatus = Field(default=TaskStatus.PENDING)
  completed_at: Optional[datetime] = None
  created_by: str
  created_at: datetime
  updated_at: datetime
  
  class Config:
    from_attributes = True

