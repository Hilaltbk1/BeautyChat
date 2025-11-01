from typing import Generator
from sqlalchemy import create_engine, QueuePool
from app.config.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(settings.DATABASE_URL, poolclass=QueuePool, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db() ->Generator[sessionmaker, None, None]:

    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()