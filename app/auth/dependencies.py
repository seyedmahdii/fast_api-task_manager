import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.jwt import verify_token
from app.schemas.user import UserInToken

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserInToken:
  """Dependency to get current authenticated user"""
  try:
    user_data = verify_token(credentials.credentials)
    if not user_data:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
      )
    return user_data
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Authentication error: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )