# This file is responsible for handling message storage and retrieval
# This function returns the inbox (latest message per conversation)

from sqlalchemy.orm import Session
from app.models.message import Message
from sqlalchemy import or_ , func , case
from app.models.user import User


def create_message(db:Session, sender_id:int, receiver_id:int , content:str):
    
    message = Message(
        sender_id = sender_id,
        receiver_id = receiver_id,
        content=content
    )
    
    try:
        db.add(message)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.refresh(message)

    return message

def get_chat_history(db:Session, user1_id:int , user2_id:int):
    
    return db.query(Message).filter(
        ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) | 
        ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
    ).order_by(Message.created_at).all()
    
    
def get_inbox(db, current_user_id: int):

    subquery = db.query(
        func.max(Message.id).label("max_id")
    ).filter(
        or_(
            Message.sender_id == current_user_id,
            Message.receiver_id == current_user_id
        )
    ).group_by(
        func.least(Message.sender_id, Message.receiver_id),
        func.greatest(Message.sender_id, Message.receiver_id)
    ).subquery()

    messages = db.query(Message , User).join(
        subquery,
        Message.id == subquery.c.max_id
    ).join(
        User,
        User.id == case(
            (
                Message.sender_id == current_user_id,
                Message.receiver_id
            ),
            else_=  Message.sender_id
        )    
    ).order_by(Message.created_at.desc()).all()

    return messages

def mark_messages_as_seen(db, user_id, other_user_id):
    messages = db.query(Message).filter(
        Message.sender_id == other_user_id,
        Message.receiver_id == user_id,
        Message.seen == False
    ).all()

    for msg in messages:
        msg.seen = True

    db.commit()

    return True

    
def get_unread_count(db, user_id, other_user_id):
    return db.query(Message).filter(
        Message.sender_id == other_user_id,
        Message.receiver_id == user_id,
        Message.seen == False
    ).count()
    