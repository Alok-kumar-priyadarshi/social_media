# This file is responsible for:
# - Creating the database engine
# - Managing database sessions
# - Providing a reusable DB dependency for APIs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()


