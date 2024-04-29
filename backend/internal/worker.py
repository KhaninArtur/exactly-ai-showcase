import asyncio

from internal.db import get_db
from internal.logging import get_logger
from internal.service.image import retrieve_image

logger = get_logger()


async def run():
    while True:
        try:
            db = next(get_db())
            retrieve_image(db)
        except Exception:
            logger.exception("Exception during image retrieve occurred")
        await asyncio.sleep(60)
