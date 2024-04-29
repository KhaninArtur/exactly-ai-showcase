from typing import Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from internal.db.models import Image


def create_image(db: Session, image_id: str) -> Image:
    image = Image(id=image_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_latest_images(db: Session, limit: int | None = None) -> list[Type[Image]]:
    query = db.query(Image).order_by(desc(Image.created_at))
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_total_images(db: Session) -> int:
    return db.query(Image).count()
