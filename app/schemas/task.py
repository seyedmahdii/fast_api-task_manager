from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskModel

class TaskBase(TaskModel):
  pass
  
class TaskCreate(BaseModel):
  title: str
  created_by: str

class TaskUpdate(BaseModel):
  title: Optional[str] = str
  status: Optional[TaskStatus] = None
  completed_at: Optional[datetime] = None

class TaskResponse(TaskModel):
  class Config:
    from_attributes = True
