from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.message_service import (
    get_chat_history,
    get_unread_count,
    get_inbox,
    mark_messages_as_seen
)
from app.models.user import User
from app.models.follow import Follow

router = APIRouter(prefix="/messages")


# 🔥 EXISTING CHATS (INBOX)
@router.get("/inbox")
def inbox(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    results = get_inbox(db, current_user.id)

    return [
        {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "last_message": message.content if message else None,
            "timestamp": message.created_at if message else None,
            "unread_count": get_unread_count(db, current_user.id, user.id)
        }
        for message, user in results
    ]

@router.get("/users")
def get_chat_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # users you follow
    following = db.query(Follow).filter(
        Follow.follower_id == current_user.id
    ).all()

    # users who follow you
    followers = db.query(Follow).filter(
        Follow.following_id == current_user.id
    ).all()

    user_ids = set()

    for f in following:
        user_ids.add(f.following_id)

    for f in followers:
        user_ids.add(f.follower_id)

    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return [
        {
            "id": u.id,
            "username": u.username
        }
        for u in users
    ]

# 🔥 CHAT HISTORY
@router.get("/{user_id}")
def get_message(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    mark_messages_as_seen(db, current_user.id, user_id)

    messages = get_chat_history(db, current_user.id, user_id)

    return [
        {
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "content": m.content,
            "seen": m.seen,
            "created_at": m.created_at
        }
        for m in messages
    ]
