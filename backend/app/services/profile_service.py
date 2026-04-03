# This file is responsible for fetching user profile data
# including followers and following count, with block checks

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.follow import Follow
from app.services.block_service import can_interact


def get_user_profile(db:Session, current_user_id:int, target_user_id:int):
    
    if not can_interact(db, current_user_id, target_user_id):
        return None
    
    user = db.query(User).filter(User.id == target_user_id).first()
    
    if not user or not user.is_active:
        return None
    
    followers_count = db.query(func.count(Follow.id)).filter(
        Follow.following_id == target_user_id
    ).scalar()

    following_count = db.query(func.count(Follow.id)).filter(
        Follow.follower_id == target_user_id
    ).scalar()
    
    return {
        "id": user.id,
        "username":user.username,
        "bio":user.bio,
        "followers": followers_count,
        "following":following_count
    }


