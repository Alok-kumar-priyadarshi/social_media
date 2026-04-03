# This file is responsible for defining the Like relationship
# between users and posts

from sqlalchemy import Column, Integer , ForeignKey , UniqueConstraint
from app.db.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer,primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer , ForeignKey("posts.id"),nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id" , "post_id" , name="unique_like"),
    )

