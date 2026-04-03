# This file is responsible for handling block/unblock logic

from sqlalchemy.orm import Session
from app.models.block import Block
from app.models.follow import Follow

def block_user(db:Session, current_user_id:int,target_user_id:int):
    if current_user_id == target_user_id:
        return None
    
    existing= db.query(Block).filter(
        Block.blocker_id == current_user_id,
        Block.blocked_id == target_user_id
    ).first()

    if existing:
        return existing
    
    db.query(Follow).filter(
        (Follow.follower_id == current_user_id) & (Follow.following_id == target_user_id)
    ).delete()

    db.query(Follow).filter(
        (Follow.follower_id == target_user_id)&(Follow.following_id == current_user_id)
    ).delete()

    block = Block(
        blocker_id = current_user_id,
        blocked_id = target_user_id
    )
    
    db.add(block)
    db.commit()
    db.refresh(block)

    return block


def unblock_user(db:Session, current_user_id:int, target_user_id:int):
    block = db.query(Block).filter(
        Block.blocker_id == current_user_id,
        Block.blocked_id == target_user_id
    ).first()

    if not block:
        return False
    
    db.delete(block)
    db.commit()

    return True

def is_blocked(db:Session , user1_id:int, user2_id:int):
    return db.query(Block).filter(
        ((Block.blocker_id == user1_id) & (Block.blocked_id == user2_id)) |
        ((Block.blocker_id == user2_id) & (Block.blocked_id == user1_id))
    ).first() is not None

def can_interact(db,user1_id:int, user2_id:int)->bool:
    return not db.query(Block).filter(
        ((Block.blocker_id == user1_id) & (Block.blocked_id == user2_id)) |
        ((Block.blocker_id == user2_id) & (Block.blocked_id == user1_id))
    ).first()



