from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from api.image import ImageResponse
from internal.db import get_db
from main import app


@pytest.fixture
def client(session_mock):
    app.dependency_overrides[get_db] = lambda: session_mock
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_get_images_success(client):
    with patch("api.image.get_logger") as logger_mock, patch(
        "internal.service.image.get_latest_images"
    ) as service_mock:
        logger_mock.return_value = MagicMock()
        service_mock.return_value = (
            [ImageResponse(id="1", created_at=datetime.now())],  # cat images
            [ImageResponse(id="2", created_at=datetime.now())],  # dog images
            2,  # total images
            datetime.now(),  # last retrieve at
        )
        response = client.get("/images")
        assert response.status_code == 200
        data = response.json()
        assert data["total_images"] == 2


@pytest.mark.asyncio
async def test_get_images_failure(client):
    with patch("api.image.get_logger") as logger_mock, patch(
        "internal.service.image.get_latest_images",
        side_effect=Exception("DB error"),
    ):
        logger_mock.return_value = MagicMock()
        response = client.get("/images")
        assert response.status_code == 500
        assert response.json()["detail"] == "Something went wrong"
