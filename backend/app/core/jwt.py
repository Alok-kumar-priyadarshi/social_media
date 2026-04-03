# This file is responsible for creating and decoding JWT tokens
# used for user authentication.

from datetime import datetime , timedelta
from jose import jwt, JWTError

from app.core.config import settings

def create_access_token(data:dict,expires_delta:timedelta = None):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        return payload
    except JWTError:
        return None