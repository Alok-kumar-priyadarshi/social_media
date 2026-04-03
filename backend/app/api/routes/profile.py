# This file is responsible for handling profile-related API endpoints

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.profile_service import get_user_profile


router = APIRouter(prefix = "/profile")


@router.get("/{user_id}")
def get_profile(
    user_id:int,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    profile = get_user_profile(db , current_user.id , user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    return profile

