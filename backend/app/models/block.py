# This file is responsible for defining the block relationship
# between users (who blocks whom)

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.database import Base

class Block(Base):
    
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True)

    blocker_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blocked_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("blocker_id" , "blocked_id" , name="unique_block"),
    )
    