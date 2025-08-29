from passlib.context import CryptContext
from passlib.exc import UnknownHashError

# Create password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  """Hash a password using bcrypt"""
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> str:
  """Verify a password against a hashed password"""
  try:
    return pwd_context.verify(plain_password, hashed_password)
  except UnknownHashError:
    return False
  
def is_password_strong(password: str) -> bool:
  """Check if a password is strong enough"""
  # return pwd_context.pwd_strenght(password) >= 3
  if len(password) < 8:
    return False
  
  # Check for at least one uppercase, lowercase, digit, and special char
  has_upper = any(c.isupper() for c in password)
  has_lower = any(c.islower() for c in password)
  has_digit = any(c.isdigit() for c in password)
  has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
  
  return has_upper and has_lower and has_digit and has_special
  
