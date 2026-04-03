# This file is responsible for handling follow-related queries like
# fetching followers and following lists with pagination

from sqlalchemy.orm import Session
from app.models.follow import Follow
from app.services.block_service import can_interact
from app.models.user import User
from app.models.block import Block
from sqlalchemy import or_

def follow_user(db: Session, current_user_id: int, target_user_id:int):
    
    if not can_interact(db, current_user_id, target_user_id):
        return "Blocked"
    
    if current_user_id == target_user_id:
        return None
    
    existing = db.query(Follow).filter(
        Follow.follower_id == current_user_id,
        Follow.following_id == target_user_id
    ).first()

    if existing:
        return existing
    
    follow = Follow(
        follower_id = current_user_id,
        following_id = target_user_id
    )
    
    db.add(follow)
    db.commit()
    db.refresh(follow)

    return follow

def unfollow_user(db:Session, current_user_id: int, target_user_id:int):
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user_id,
        Follow.following_id == target_user_id
    ).first()

    if not follow:
        return False
    
    db.delete(follow)
    db.commit()

    return True

def get_followers(db ,current_user_id:int, user_id: int, limit:int, offset:int):

    return db.query(User).join(
        Follow, Follow.follower_id == User.id
    ).filter(
        Follow.following_id == user_id,
        ~db.query(Block).filter(
            or_(
                (Block.blocker_id == current_user_id) & (Block.blocked_id == User.id),
                (Block.blocker_id == User.id) & (Block.blocked_id == current_user_id)
            )
        ).exists()
    ).offset(offset).limit(limit).all()



def get_following(db , current_user_id:int, user_id:int , limit:int, offset: int):
    return db.query(User).join(
        Follow, Follow.following_id == User.id
    ).filter(
        Follow.follower_id == user_id,
        ~db.query(Block).filter(
            or_(
                (Block.blocker_id == current_user_id) & (Block.blocked_id == User.id),
                (Block.blocker_id == User.id) & (Block.blocked_id == current_user_id)
            )
        ).exists()
    ).offset(offset).limit(limit).all()