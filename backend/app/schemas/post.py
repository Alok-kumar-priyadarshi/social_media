# This file is responsible for defining schemas for post creation and response

from pydantic import BaseModel

class PostCreate(BaseModel):
    caption: str | None = None
    image_url: str| None = None
    
class PostResponse(BaseModel):
    id:int
    caption:str |None
    image_url:str |None
    user_id : int

    class Config:
        from_attributes = True