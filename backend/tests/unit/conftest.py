# backend/tests/unit/conftest.py
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

# Добавляем backend в путь
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(root_dir / "backend"))

# Импортируем только если нужны для unit тестов
try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None  # type: ignore


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables for all tests."""
    os.environ.setdefault("POSTGRES_HOST", "localhost")
    os.environ.setdefault("POSTGRES_PORT", "5432")
    os.environ.setdefault("POSTGRES_USER", "test_user")
    os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
    os.environ.setdefault("POSTGRES_DB", "test_db")
    os.environ.setdefault("DB_USE_SSL", "false")
    os.environ.setdefault("SWAGGER_PATH", "/swagger")
    os.environ.setdefault("APP_NAME", "mood-tracker-backend-test")
    
    yield


@pytest.fixture
def mock_db_session():
    """Create a mock database session for unit tests."""
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.close = AsyncMock()
    return session


@pytest.fixture
def sample_mood_entry():
    """Create a sample mood entry for testing."""
    from datetime import datetime
    from app.db.models.track import MoodTrack
    
    return MoodTrack(
        username="test_user",
        mood_entry=4,
        comment="Feeling great!",
        created_at=datetime.now()
    )