# This file is responsible for handling business logic related to posts

from sqlalchemy.orm import Session
from app.models.post import Post

def create_post(db:Session,user_id:int,caption:str, image_url:str):
    
    if not caption and not image_url:
        return None
    
    post = Post(
        user_id = user_id,
        caption = caption,
        image_url=image_url
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)

    return post