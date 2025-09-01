import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt import verify_token
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.schemas.user import UserInToken
from app.services.task_service import TaskService
from app.auth.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["Tasks"])
security = HTTPBearer()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, current_user: UserInToken = Depends(get_current_user)):
  """Create a new task for the current user"""
  try:
    task_service = TaskService()
    new_task = await task_service.create_task(task_data,  current_user.id)
    logger.info(f"New task created: {new_task}")
    
    return new_task
  except HTTPException:
    raise
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))    
  except Exception as e:
    logger.error(f"Error creating a new task: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )
    
@router.get("/", response_model=List[TaskResponse])
async def get_current_user_tasks(current_user: UserInToken = Depends(get_current_user)):
  """Get all tasks of current user"""
  try:    
    task_service = TaskService()
    tasks = await task_service.get_user_all_tasks(current_user.id)
    logger.info(f"All tasks retrieved")
    
    return tasks
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error getting all tasks: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )
    
@router.delete("/{task_id}")
async def delete_task(task_id: str, current_user: UserInToken = Depends(get_current_user)):
  """Delete a task"""
  try:
    task_service = TaskService()
    success = await task_service.delete_task(task_id)
    if not success:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
      )
    logger.info(f"Task {task_id} deleted by {current_user.email}")
    return {"message": "Task deleted successfully"}
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error deleting task: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )

@router.patch("/{task_id}", response_model=TaskUpdate)
async def update_task(
  task_id: str, 
  task_data: TaskUpdate,
  current_user: UserInToken = Depends(get_current_user)
):
  """Update a task"""
  try:
    task_service = TaskService()
    updated_task = await task_service.update_task(task_id, task_data)
    if not updated_task:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
      )
    logger.info(f"Task {task_id} updated by {current_user.email}")
    return updated_task
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error deleting task: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )