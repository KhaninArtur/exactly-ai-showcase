from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.image import router as image_router
from internal.db import create_database
from internal.logging import setup_logging
from internal.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    setup_logging()
    yield


app = FastAPI(debug=settings.debug, lifespan=lifespan)
app.include_router(image_router)

if __name__ == "__main__":
    uvicorn.run(app, access_log=False)
