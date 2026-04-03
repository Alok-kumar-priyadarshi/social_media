# This file handles comment APIs

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.comment import Comment
from app.api.deps import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


#  Add comment
@router.post("/{post_id}")
def add_comment(
    post_id: int,
    content: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    comment = Comment(
        user_id=current_user.id,
        post_id=post_id,
        content=content
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


#  Get comments of a post
@router.get("/{post_id}")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(Comment.created_at.desc()).all()

    return comments