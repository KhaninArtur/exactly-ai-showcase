from datetime import datetime
from unittest.mock import patch

import pytest
import requests

from internal.db.models import AnimalType, Image
from internal.service.exception import ExternalAPIException, DBException
from internal.service.image import (
    _fetch_image_data,
    _save_image_to_cloud,
    _create_image_record,
    retrieve_image,
    get_latest_images,
)


def test_fetch_image_data_success():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = "c2FtcGxlZGF0YQ=="  # Base64 encoded "sampledata"
        assert _fetch_image_data() == b"sampledata"


def test_fetch_image_data_failure():
    with patch("requests.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = requests.RequestException(
            "API failure"
        )
        with pytest.raises(ExternalAPIException):
            _fetch_image_data()


def test_save_image_to_cloud_success():
    with patch("internal.service.image.uuid.uuid4") as mock_uuid, patch(
        "internal.service.image.save_image_cloud"
    ) as mock_save:
        mock_uuid.return_value.hex = "123"
        assert _save_image_to_cloud(b"data") == "123"
        mock_save.assert_called_once_with("123", b"data")


def test_save_image_to_cloud_failure():
    with patch("internal.service.image.uuid.uuid4") as mock_uuid, patch(
        "internal.service.image.save_image_cloud"
    ) as mock_save:
        mock_uuid.return_value.hex = "123"
        mock_save.side_effect = Exception("Cloud failure")
        with pytest.raises(ExternalAPIException):
            _save_image_to_cloud(b"data")


def test_create_image_record_success(session_mock):
    with patch("internal.service.image.db_image.create_image") as mock_create:
        _create_image_record(session_mock, "123", AnimalType.cat)
        mock_create.assert_called_once_with(session_mock, "123", AnimalType.cat)


def test_create_image_record_failure(session_mock):
    with patch("internal.service.image.db_image.create_image") as mock_create:
        mock_create.side_effect = Exception("DB failure")
        with pytest.raises(DBException):
            _create_image_record(session_mock, "123", AnimalType.cat)


def test_retrieve_image_success(session_mock):
    with patch("internal.service.image._fetch_image_data", return_value=b"data"), patch(
        "internal.service.image.classify_image", return_value=AnimalType.cat
    ), patch("internal.service.image._save_image_to_cloud", return_value="123"), patch(
        "internal.service.image._create_image_record"
    ) as mock_create:
        retrieve_image(session_mock)
        mock_create.assert_called_once_with(session_mock, "123", AnimalType.cat)


def test_get_latest_images_success(session_mock):
    with patch(
        "internal.service.image.db_image.get_latest_images",
        return_value=[Image(id="1", created_at=datetime.now())],
    ) as mock_get, patch(
        "internal.service.image.db_image.get_total_images", return_value=10
    ):
        cats, dogs, total, last_time = get_latest_images(session_mock)
        assert len(cats) == 1
        assert total == 10


def test_get_latest_images_failure(session_mock):
    with patch("internal.service.image.db_image.get_latest_images") as mock_get:
        mock_get.side_effect = Exception("DB query failure")
        with pytest.raises(DBException):
            get_latest_images(session_mock)
