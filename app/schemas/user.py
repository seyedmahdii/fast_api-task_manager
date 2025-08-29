from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base User Schema (common fields)
class UserBase(BaseModel):
  email: EmailStr
  username: str = Field(min_length=3, max_length=50)
  full_name: str = Field(min_length=2, max_length=100)
  
# User Registration Schema (what client sends when registering)
class UserCreate(UserBase):
  password: str = Field(min_length=6, description="Password must be at least 6 characters")

# User Login Schema (what client sends when logging in)
class UserLogin(BaseModel):
  email: EmailStr
  password: str
  
# User Update Schema (what client sends when updating profile)
class UserUpdate(BaseModel):
  email: Optional[EmailStr] = None
  username: Optional[str] = Field(None, min_length=3, max_length=50)
  full_name: Optional[str] = Field(None, min_length=2, max_length=100)
  password: Optional[str] = Field(None, min_length=6)

# User Response Schema (What gets sent back to client (no password!))
class UserResponse(UserBase):
  id: str
  is_active: bool
  is_superuser: bool
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True  # Allows conversion from ORM objects
    
# User in Token Schema (User data stored in JWT token)
class UserInToken(BaseModel):
  id: str
  email: str
  username: str
  is_superuser: bool
  
# Token Response Schema (What client gets after successful login)
class TokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"
  user: UserInToken