# This file is responsible for handling like/unlike logic

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.like_service import like_post, unlike_post

router = APIRouter(prefix="/likes")

@router.post("/{post_id}")
def like(post_id: int, db:Session = Depends(get_db) , current_user = Depends(get_current_user)):
    like_post(db, current_user.id , post_id)
    return {"message":"Post liked"}


@router.delete("/{post_id}")
def unlike(post_id:int, db:Session = Depends(get_db), current_user=Depends(get_current_user)):
    success = unlike_post(db, current_user.id, post_id)

    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    
    return {
        "message": "Post unliked"
    }