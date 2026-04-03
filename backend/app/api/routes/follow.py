# This file is responsible for handling follow/unfollow API endpoints

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.follow_service import follow_user, unfollow_user , get_followers , get_following

from typing import List
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/follow/{user_id}")
def follow(user_id: int, db:Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = follow_user(db, current_user.id,user_id)
    
    if result == "Blocked":
        raise HTTPException(status_code=403, detail="cannot follow a blocked User")

    if result is None:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    return {"message": "Followed successfully"}

@router.delete("/follow/{user_id}")
def unfollow(user_id:int, db:Session = Depends(get_db), current_user=Depends(get_current_user)):
    success = unfollow_user(db , current_user.id , user_id)

    if not success:
        raise HTTPException(status_code=404, detail="Not following user")
    
    return {"message": "unfollowed successfully"}

@router.get("/followers/{user_id}" , response_model=List[UserResponse])
def followers(
    user_id:int,
    limit:int = 10,
    offset:int = 0,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_followers(db , current_user.id ,user_id , limit , offset)

@router.get("/following/{user_id}" , response_model=List[UserResponse])
def following(
    user_id:int,
    limit:int = 10,
    offset:int = 0,
    db:Session = Depends(get_db),
    current_user =Depends(get_current_user)
):
    return get_following(db , current_user.id , user_id, limit , offset)
