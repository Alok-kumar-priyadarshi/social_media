# This model stores comments on posts

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    content = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())