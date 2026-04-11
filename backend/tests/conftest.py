import os
from typing import AsyncIterator, Iterator

import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    container = PostgresContainer(image="postgres:16-alpine")
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session", autouse=True)
def _set_test_env(postgres_container: PostgresContainer) -> None:
    from sqlalchemy.engine import make_url

    url = make_url(postgres_container.get_connection_url())

    os.environ["POSTGRES_HOST"] = url.host or "localhost"
    os.environ["POSTGRES_PORT"] = str(url.port or 5432)
    os.environ["POSTGRES_USER"] = url.username or "postgres"
    os.environ["POSTGRES_PASSWORD"] = url.password or "postgres"
    os.environ["POSTGRES_DB"] = (url.database or "postgres").lstrip("/")

    os.environ["DB_USE_SSL"] = "false"
    os.environ["SWAGGER_PATH"] = "/swagger"
    os.environ["REDOC_PATH"] = ""


@pytest_asyncio.fixture
async def app() -> AsyncIterator[object]:
    from app.src.app import app as fastapi_app
    yield fastapi_app
