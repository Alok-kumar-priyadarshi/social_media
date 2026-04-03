# This file is responsible for defining the Message table
# which stores chat messages between users

from sqlalchemy import Column , Boolean , Integer , ForeignKey , String , DateTime
from datetime import datetime

from app.db.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer , primary_key=True)

    sender_id = Column(Integer , ForeignKey("users.id"),nullable=False)
    receiver_id = Column(Integer , ForeignKey("users.id"), nullable=False)
    
    content = Column(String , nullable=False)

    created_at = Column(DateTime  ,default=datetime.utcnow)
    
    seen = Column(Boolean , default=False)


