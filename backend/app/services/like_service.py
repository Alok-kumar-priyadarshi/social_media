# This file is responsible for handling like/unlike logic

from sqlalchemy.orm import Session
from app.models.like import Like


def like_post(db:Session, user_id:int , post_id:int):
    
    existing = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()

    if existing:
        return existing
    
    like = Like(user_id=user_id , post_id=post_id)

    db.add(like)
    db.commit()
    db.refresh(like)

    return like


def unlike_post(db:Session, user_id:int , post_id:int):
    
    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()

    if not like:
        return False
    
    db.delete(like)
    db.commit()

    return True