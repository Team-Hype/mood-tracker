import os
import importlib
from typing import AsyncIterator, Iterator

from fastapi import FastAPI
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.engine import make_url
from testcontainers.postgres import PostgresContainer

from app.db.connection.session import get_session
from app.src.app import app as fastapi_app


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    """Start a PostgreSQL container once per test session."""
    container = PostgresContainer(image="postgres:16-alpine")
    container.start()
    try:
        yield container
    finally:
        container.stop()


@pytest.fixture(scope="session", autouse=True)
def set_test_env(postgres_container: PostgresContainer) -> None:
    """Set environment variables for the test database (once per session)."""
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


@pytest_asyncio.fixture(scope="function")
async def db_session(set_test_env) -> AsyncIterator[AsyncSession]:
    """Create a fresh database session for each test."""
    from app.src.settings import settings

    engine = create_async_engine(
        settings.database_uri,
        echo=True,
        future=True,
        connect_args=settings.db_context,
    )

    from app.db import DeclarativeBase

    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)

    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session

    await session.close()
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def app(db_session: AsyncSession) -> AsyncIterator[FastAPI]:
    """Override the get_session dependency to use the test session."""

    async def override_get_session():
        yield db_session

    fastapi_app.dependency_overrides[get_session] = override_get_session
    yield fastapi_app
    fastapi_app.dependency_overrides.clear()
