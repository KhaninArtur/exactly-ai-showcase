import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.image import router as image_router
from internal import worker
from internal.db import create_database
from internal.logging import setup_logging
from internal.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    setup_logging()
    task = asyncio.create_task(worker.run())
    yield
    task.cancel()


app = FastAPI(debug=settings.debug, lifespan=lifespan)
app.include_router(image_router)

# TODO: add this middleware only if it's local deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Specify the origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    uvicorn.run(app, access_log=False)
