# This file is responsible for handling user-related API routes like signup

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from fastapi import UploadFile, File, Form

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from app.db.database import get_db
from app.models.user import User
from app.models.post import Post
from app.api.deps import get_current_user
from app.models.follow import Follow
from fastapi import UploadFile, File
from app.api.routes.upload import upload_file


router = APIRouter()

@router.post("/signup",response_model=UserResponse)
def signup(user:UserCreate,db:Session = Depends(get_db)):
    new_user = create_user(db,user.username, user.email , user.password)

    if not new_user:
        raise HTTPException(status_code=400, detail="user already exists")
    
    return new_user


@router.put("/users/me")
async def update_profile(
    bio: str = Form(""),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        print("BIO:", bio)
        print("FILE:", file.filename if file else "no file added")

        current_user.bio = bio

        if file:
            image_url = await upload_file(file)
            current_user.profile_picture = image_url["url"]

        db.commit()
        db.refresh(current_user)

        return {"message": "updated"}

    except Exception as e:
        print("ERROR:", str(e))   # 🔥 IMPORTANT
        raise
    
    

@router.get("/users/me")
def get_me(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    followers_count = db.query(Follow).filter(
        Follow.following_id == current_user.id
    ).count()

    following_count = db.query(Follow).filter(
        Follow.follower_id == current_user.id
    ).count()

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "followers_count": followers_count,
        "following_count":  following_count,
        "profile_image":current_user.profile_picture
    }


# 🧵 Get posts of a specific user
@router.get("/users/{user_id}/posts")
def get_user_posts(user_id: int, db: Session = Depends(get_db)):

    # 🔹 Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔹 Get posts (latest first)
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(Post.created_at.desc())  # IMPORTANT
        .all()
    )

    return [
        {
            "id": p.id,
            "image_url": p.image_url,
            "caption": p.caption,
            "created_at": p.created_at,
        }
        for p in posts
    ]
    
    
    
@router.get("/users/search")
def search_users(query: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(
        User.username.ilike(f"%{query}%")
    ).all()

    return [
        {
            "id": u.id,
            "username": u.username
        }
        for u in users
    ]
    
    
    
    