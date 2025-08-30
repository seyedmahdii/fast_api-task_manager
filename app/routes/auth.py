from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse, UserInToken
from app.services import user_service
from app.services.user_service import UserService
from app.auth.password import is_password_strong
from app.auth.jwt import create_access_token, create_user_token_data, verify_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
  """Register a new user"""
  try:
    if not is_password_strong(user_data.password):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number"
      )
    
    user_service = UserService()
    new_user = await user_service.create_user(user_data)
    logger.info(f"New user registered: {new_user}")
    return new_user

  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(e)
    )
  except Exception as e:
    logger.error(f"Error registering user: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )
    
@router.post("/login", response_model=TokenResponse)
async def login_user(user_data: UserLogin):
  """Login user and return JWT token"""
  try:
    user_service = UserService()
    user = await user_service.authenticate_user(user_data.email, user_data.password)
    
    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
      )
    
    if not user.is_active:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Account is deactivated"
      )
    
    token_data = create_user_token_data(
      user_id=str(user.id),
      email=user.email,
      username=user.username,
      is_superuser=user.is_superuser
    )
    access_token = create_access_token(data=token_data)
    
    token_response = TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserInToken(
            id=str(user.id),
            email=user.email,
            username=user.username,
            is_superuser=user.is_superuser
        )
    )
    
    logger.info(f"User logged in: {user.email}")
    return token_response
  
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error logging in user: {e}")
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Internal server error"
    )
    
@router.post("/logout")
async def logout_user():
    """Logout user (invalidate token)"""
    # TODO: Implement token blacklisting
    return {"message": "Successfully logged out"}
  
@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
  """Get current authenticated user"""
  try:
    user_data = verify_token(credentials.credentials)
    if not user_data:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
      )
      
    user_service = UserService()
    user = await user_service.get_user_by_id(user_data.id)
    if not user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
      )
    return UserResponse(
      id=str(user.id),
      email=user.email,
      username=user.username,
      full_name=user.full_name,
      is_active=user.is_active,
      is_superuser=user.is_superuser,
      created_at=user.created_at,
      updated_at=user.updated_at
    )
  
  except HTTPException:
    raise
  except Exception as e:
    logger.error(f"Error getting current user: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error"
    )