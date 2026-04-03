# This file is responsible for defining the Post table
# which stores user-generated content like images and captions


from sqlalchemy import Column , Integer , String , ForeignKey , DateTime
from datetime import datetime

from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer , primary_key=True , index=True)
    
    user_id = Column(Integer , ForeignKey("users.id") , nullable=True)

    caption = Column(String , nullable = True)
    image_url = Column(String , nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


