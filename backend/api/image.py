from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from internal.db import get_db
from internal.logging import get_logger
from internal.service import image as image_service
from internal.settings import settings


class ImageResponse(BaseModel):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ImagesResponse(BaseModel):
    images: list[ImageResponse]
    total_images: int


router = APIRouter()
logger = get_logger()


@router.get("/images")
async def get_images(
    db: Session = Depends(get_db),
    after: datetime = Query(None, alias="after"),
    limit: int = Query(settings.images_limit, ge=1, le=100),
) -> ImagesResponse:
    logger.info(f"Fetching images with after={after} and limit={limit}")
    try:
        images_list, total_images = image_service.get_latest_images(db, after, limit)
    except Exception as e:
        logger.error(f"Failed to get images: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")
    return ImagesResponse(images=images_list, total_images=total_images)