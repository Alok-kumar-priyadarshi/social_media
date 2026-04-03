# This file is responsible for handling business logic related to posts

from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import create_post
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.follow import Follow
from app.models.post import Post
from app.models.like import Like
from app.models.user import User
from app.models.block import Block


router = APIRouter(prefix="/posts")


@router.post("/" , response_model=PostResponse)

def create_new_post(
    post:PostCreate,
    db:Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_post = create_post(
        db,
        current_user.id,
        post.caption,
        post.image_url
    )
    
    if not new_post:
        raise HTTPException(status_code=400 , detail="post cannot be empty")
    
    return new_post

# This endpoint returns paginated feed posts (infinite scroll ready)

@router.get("/feed")
def get_feed(
    offset: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1️⃣ Get following users
    following = db.query(Follow).filter(
        Follow.follower_id == current_user.id
    ).all()

    following_ids = [f.following_id for f in following]

    # 2️⃣ Get blocked users (both directions)
    blocked = db.query(Block).filter(
        (Block.blocker_id == current_user.id) |
        (Block.blocked_id == current_user.id)
    ).all()

    blocked_ids = set()
    for b in blocked:
        blocked_ids.add(b.blocked_id)
        blocked_ids.add(b.blocker_id)

    # 3️⃣ Remove blocked users from feed
    valid_ids = [
        uid for uid in following_ids
        if uid not in blocked_ids
    ]

    # include yourself
    valid_ids.append(current_user.id)

    # 4️⃣ Fetch posts
    posts = (
        db.query(Post)
        .filter(Post.user_id.in_(valid_ids))
        .order_by(Post.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for p in posts:
        user = db.query(User).filter(User.id == p.user_id).first()

        like_count = db.query(Like).filter(Like.post_id == p.id).count()

        is_liked = db.query(Like).filter(
            Like.post_id == p.id,
            Like.user_id == current_user.id
        ).first() is not None

        result.append({
            "id": p.id,
            "image_url": p.image_url,
            "caption": p.caption,
            "user_id": p.user_id,
            "like_count": like_count,
            "is_liked": is_liked,
            "username": user.username
        })

    return result