from datetime import datetime, timezone
import logging
from typing import Optional, List

from bson import ObjectId

from app.database import get_collection
from app.models.task import TaskModel, TaskStatus
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

logger = logging.getLogger(__name__)

class TaskService:
  def __init__(self):
    self.collection = get_collection("tasks")
  
  async def create_task(self, task_data: TaskCreate, created_by: str) -> TaskResponse:
    """Create a new task"""
    try:
      new_task = {
        "title": task_data.title,
        "status": TaskStatus.PENDING,
        "created_by": created_by,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
      }
      result = await self.collection.insert_one(new_task)
      created_task = await self.collection.find_one({"_id": result.inserted_id})

      return TaskResponse(
        id=str(created_task["_id"]),
        title=created_task["title"],
        status=created_task["status"],
        created_by=created_task["created_by"],
        completed_at=created_task.get("completed_at"),
        created_at=created_task["created_at"],
        updated_at=created_task["updated_at"],
      )
    except Exception as e:
      logger.error(f"Error creating task: {e}")
      raise
  
  async def get_task_by_id(self, task_id: str) -> Optional[TaskModel]:
    """Get a task by task id"""
    try:
      task_doc = await self.collection.find_one({"_id": ObjectId(task_id)})
      if task_doc:
        return TaskModel(**task_doc)
      return None
    except Exception as e:
      logger.error(f"Error getting task by id: {e}")
      raise
    
  async def update_task(self, task_id: str, task_data: TaskUpdate) -> Optional[TaskResponse]:
    """Update a task"""
    try:
      updated_task = {}
      
      if task_data.title is not None:
        updated_task["title"] = task_data.title
      if task_data.status is not None:
        updated_task["status"] = task_data.status
      if task_data.completed_at is not None:
        updated_task["completed_at"] = task_data.completed_at
      updated_task["updated_at"] = datetime.now(timezone.utc)
      
      result = await self.collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": updated_task}
      )
      if result.modified_count > 0:
        task = await self.get_task_by_id(task_id)
        return TaskResponse(
          id=str(task["_id"]),
          title=task["title"],
          status=task["status"],
          created_by=task["created_by"],
          completed_at=task.get("completed_at"),
          created_at=task["created_at"],
          updated_at=task["updated_at"],
        )
      return None
    except Exception as e:
      logger.error(f"Error updating a task: {e}")
      raise
  
  # What this function will return?
  async def delete_task(self, task_id: str) -> bool:
    """Delete a task by task id"""
    try:
      result = await self.collection.delete_one({"_id": ObjectId(task_id)})
      return result.acknowledged
    except Exception as e:
      logger.error(f"Error deleting a task: {e}")
      raise
  
  async def get_user_all_tasks(self, user_id: str, skip: int = 0, limit: int = 50) -> List[TaskResponse]:
    """Get all tasks of a user"""
    try: 
      cursor = self.collection.find({"created_by": user_id}).skip(skip).limit(limit)
      tasks = []
      async for doc in cursor:
        tasks.append(TaskResponse(
          id=str(doc["_id"]),
          title=doc["title"],
          status=doc["status"],
          created_by=doc["created_by"],
          completed_at=doc.get("completed_at"),
          created_at=doc["created_at"],
          updated_at=doc["updated_at"],
        ))
      return tasks
    except Exception as e:
      logger.error(f"Error all tasks of a user: {e}")
      raise