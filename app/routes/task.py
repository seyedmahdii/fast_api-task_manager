import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt import verify_token
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["Tasks"])
security = HTTPBearer()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, credentials: HTTPAuthorizationCredentials=Depends(security)):
  """Create a new task for the current user"""
  try:
    user_data = verify_token(credentials.credentials)
    if not user_data:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
      )

    task_service = TaskService()
    new_task = await task_service.create_task(task_data,  user_data.id)
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
async def get_current_user_tasks(credentials: HTTPAuthorizationCredentials=Depends(security)):
  """Get all tasks of current user"""
  try:
    user_data = verify_token(credentials.credentials)
    if not user_data:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
      )
    
    task_service = TaskService()
    tasks = await task_service.get_user_all_tasks(user_data.id)
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