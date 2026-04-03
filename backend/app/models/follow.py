# This file is responsible for defining the follow relationship
# between users (who follows whom)

from sqlalchemy import Column, Integer , ForeignKey,UniqueConstraint
from app.db.database import Base

class Follow(Base):
    __tablename__ = "follows"
    
    id = Column(Integer, primary_key=True)

    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer , ForeignKey("users.id") , nullable=False)

    __table_args__ = (
        UniqueConstraint("follower_id","following_id", name="unique_follow"),
    )



