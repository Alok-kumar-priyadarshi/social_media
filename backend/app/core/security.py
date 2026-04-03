# What this file does:
# - Handles password hashing and verification
# - Creates and verifies JWT tokens

# Why it exists:
# - Centralizes all security logic (auth-related)
# - Avoids duplication across services

# How it interacts:
# - Used by auth service for login/register
# - Used in protected routes for token validation

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt , JWTError
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password:str, hashed:str)-> bool:
    return pwd_context.verify(password,hashed)

def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None

