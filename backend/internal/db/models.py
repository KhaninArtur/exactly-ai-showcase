from datetime import datetime

from sqlalchemy import create_engine, String, Column, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

from internal.settings import settings

engine = create_engine(
    settings.database_url,
    pool_size=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
