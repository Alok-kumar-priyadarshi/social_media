# This file is responsible for handling block/unblock API endpoints

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.block_service import block_user, unblock_user
from app.models.block import Block
from app.models.user import User


router = APIRouter(prefix="/block")

@router.post("/{user_id}")
def block(user_id: int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = block_user(db, current_user.id, user_id)

    if result is None:
        raise HTTPException(status_code=400, detail="canot block yourself")
    return {
        "message": "User blocked successfully"
    }

@router.delete("/{user_id}")
def unblock(user_id:int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    success = unblock_user(db, current_user.id, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not blocked")

    return {
        "message": "user unblocked successfully"
    }

@router.get("/")
def get_blocked_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    blocks = db.query(Block).filter(
        Block.blocker_id == current_user.id
    ).all()

    result = []

    for b in blocks:
        user = db.query(User).filter(User.id == b.blocked_id).first()

        if user:
            result.append({
                "id": user.id,
                "username": user.username
            })

    return result