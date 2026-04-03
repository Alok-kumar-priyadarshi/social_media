# What this file does:
# - Defines request/response structure for user APIs

# Why it exists:
# - Separates DB models from API layer
# - Ensures validation and clean API contracts

# How it interacts:
# - Used in routes for request validation

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True