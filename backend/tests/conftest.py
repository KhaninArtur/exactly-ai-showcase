from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from internal.settings import settings


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    settings.test_mode = True
    yield
    settings.test_mode = False


@pytest.fixture(scope="module")
def session_mock():
    session = MagicMock(spec=Session)
    return session
