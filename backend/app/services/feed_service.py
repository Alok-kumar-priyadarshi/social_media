# This file is responsible for generating the user feed
# enriched with like count and user-like status


from sqlalchemy.orm import Session
from sqlalchemy import desc , or_ , func

from app.models.post import Post
from app.models.follow import Follow
from app.models.block import Block
from app.models.like import Like

def get_feed(db:Session, current_user_id: int, limit:int , offset:int):
    following_subquery = db.query(Follow.following_id).filter(
        Follow.follower_id == current_user_id
    )
    
    like_count_subquery = db.query(
        Like.post_id,
        func.count(Like.id).label("like_count")
    ).group_by(Like.post_id).subquery()

    liked_subquery = db.query(Like.post_id).filter(
        Like.user_id == current_user_id
    ).subquery()

    query = db.query(
        Post,
        func.coalesce(like_count_subquery.c.like_count, 0).label("like_count"),
        (liked_subquery.c.post_id != None).label("is_liked")
    ).outerjoin(
        like_count_subquery,
        Post.id == like_count_subquery.c.post_id
    ).outerjoin(
        liked_subquery,
        Post.id == liked_subquery.c.post_id
    ).filter(
        or_(
            Post.user_id.in_(following_subquery),
            Post.user_id == current_user_id
        )
    )
    
    query = query.filter(
        ~db.query(Block).filter(
            ((Block.blocker_id == current_user_id) & (Block.blocked_id == Post.user_id)) |
            ((Block.blocker_id == Post.user_id) & (Block.blocked_id == current_user_id))
        ).exists()
    )
    
    results = query.order_by(desc(Post.created_at))\
        .offset(offset)\
        .limit(limit)\
        .all()
        
        
    feed = []
    
    for post , like_count , is_liked in results:
        
        feed.append({
            "id":post.id,
            "caption":post.caption,
            "image_url": post.image_url,
            "user_id": post.user_id,
            "like_count": like_count,
            "is_liked": bool(is_liked)
        })
        return feed

    
    
    
    