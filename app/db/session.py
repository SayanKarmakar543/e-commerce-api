from sqlalchemy import create_engine
from app.core.config import config_settings
from sqlalchemy.orm import sessionmaker, Session
from typing import Annotated
from fastapi import Depends

engine = create_engine(
    config_settings.SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
