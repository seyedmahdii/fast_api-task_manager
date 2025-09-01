from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.schemas.user import UserInToken
import os

SECRET_KEY = "your-secret-key-here-change-in-production"  # TODO: Move to environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  
def verify_token(token: str) -> Optional[UserInToken]:
  """Verify JWT token and return user data"""
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get("sub")
    email: str = payload.get("email")
    username: str = payload.get("username")
    is_superuser: bool = payload.get("is_superuser", False)
    
    if user_id is None or email is None or username is None:
        return None
        
    return UserInToken(
        id=user_id,
        email=email,
        username=username,
        is_superuser=is_superuser
    )
  except JWTError:
    return None
  

def create_user_token_data(user_id: str, email: str, username: str, is_superuser: bool) -> dict:
  """Create token payload for user"""
  return {
    "sub": user_id,  # Subject (user ID)
    "email": email,
    "username": username,
    "is_superuser": is_superuser
  }