import asyncio

from internal.db import get_db
from internal.service.image import retrieve_image


async def run():
    while True:
        # TODO: add try except
        db = next(get_db())
        retrieve_image(db)
        await asyncio.sleep(60)
