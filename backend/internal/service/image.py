import uuid
from base64 import b64decode
from datetime import datetime
from typing import Type

import requests
from sqlalchemy.orm import Session

from internal.db import image as db_image
from internal.db.models import Image, AnimalType
from internal.logging import get_logger
from internal.service.exception import DBException, ExternalAPIException
from internal.service.image_classifier import classify_image
from internal.service.utils import save_image_cloud
from internal.settings import settings

logger = get_logger()

last_retrieve_at: datetime = datetime.utcnow()


def retrieve_image(db: Session):
    global last_retrieve_at
    image_data = _fetch_image_data()
    image_type = classify_image(image_data)
    image_id = _save_image_to_cloud(image_data)
    _create_image_record(db, image_id, image_type)
    last_retrieve_at = datetime.utcnow()


def _fetch_image_data():
    logger.debug("Fetching image data from external API")
    try:
        response = requests.post(settings.exactly_api)
        response.raise_for_status()
        return b64decode(response.text)
    except requests.RequestException as e:
        logger.error(f"Failed to fetch image data: {str(e)}")
        raise ExternalAPIException(detail=str(e))


def _save_image_to_cloud(image_data):
    logger.debug("Saving image data to cloud")
    try:
        image_id = uuid.uuid4().hex
        save_image_cloud(image_id, image_data)
        return image_id
    except Exception as e:
        logger.error(f"Failed to save image to cloud: {str(e)}")
        raise ExternalAPIException(detail=str(e))


def _create_image_record(db: Session, image_id: str, image_type: AnimalType):
    logger.debug("Creating image record in database")
    try:
        db_image.create_image(db, image_id, image_type)
    except Exception as e:
        logger.error(f"Failed to create image record: {str(e)}")
        raise DBException(detail=str(e))


def get_latest_images(
    db: Session, limit: int | None = None
) -> tuple[list[Type[Image]], list[Type[Image]], int, datetime]:
    logger.debug("Getting latest images from the database")
    try:
        cat_images = db_image.get_latest_images(db, AnimalType.cat, limit)
        dog_images = db_image.get_latest_images(db, AnimalType.dog, limit)
        total_images = db_image.get_total_images(db)
    except Exception as e:
        logger.exception("Error fetching images")
        raise DBException(detail=str(e))
    return cat_images, dog_images, total_images, last_retrieve_at
