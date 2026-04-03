# This file is responsible for handling business logic related to users

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password , verify_password

def create_user(db:Session, username:str , email:str, password:str):
    
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing_user:
        return None
    
    hashed = hash_password(password)
    
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    
    if not verify_password(password,user.hashed_password):
        return None
    
    return user

    