from datetime import datetime
from enum import Enum

from sqlalchemy import (
    create_engine,
    String,
    Column,
    DateTime,
    Enum as SQLEnum,
    Index,
    NullPool,
)
from sqlalchemy.orm import sessionmaker, declarative_base

from internal.settings import settings

engine = create_engine(
    settings.database_url,
    connect_args={
        "check_same_thread": False
    },  # Allow use of the DB with multiple threads
    poolclass=NullPool,  # Disable pooling
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class AnimalType(Enum):
    cat = 0
    dog = 1


class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(SQLEnum(AnimalType), nullable=False)

    __table_args__ = (Index("idx_category_created_at", category, created_at.desc()),)
