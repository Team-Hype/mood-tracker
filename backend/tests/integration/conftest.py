import os
import importlib
from typing import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from sqlalchemy.engine import make_url
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    container = PostgresContainer(image="postgres:16-alpine")
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session")
def set_test_env(postgres_container: PostgresContainer) -> None:
    url = make_url(postgres_container.get_connection_url())

    os.environ["POSTGRES_HOST"] = url.host or "localhost"
    os.environ["POSTGRES_PORT"] = str(url.port or 5432)
    os.environ["POSTGRES_USER"] = url.username or "postgres"
    os.environ["POSTGRES_PASSWORD"] = url.password or "postgres"
    os.environ["POSTGRES_DB"] = (url.database or "postgres").lstrip("/")

    os.environ["DB_USE_SSL"] = "false"
    os.environ.setdefault("SWAGGER_PATH", "/swagger")

    import app.src.settings as settings_module
    importlib.reload(settings_module)

    from app.db.connection.session import SessionManager
    SessionManager().refresh()


@pytest_asyncio.fixture
async def app(set_test_env) -> AsyncIterator[object]:
    from app.src.app import app as fastapi_app
    yield fastapi_app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def dispose_engine_at_end():
    yield
    from app.db.connection.session import SessionManager
    await SessionManager().engine.dispose()
