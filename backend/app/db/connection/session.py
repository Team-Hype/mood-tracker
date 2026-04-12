__all__ = ["get_session", "SessionDependency"]

from threading import Lock
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
)
from app.src.settings import settings


class SessionManager:
    _instance = None
    _lock = Lock()
    session_maker: async_sessionmaker | None = None  # changed
    engine: AsyncEngine

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(SessionManager, cls).__new__(cls)
                cls._instance.refresh()
            return cls._instance

    def get_session_maker(self) -> async_sessionmaker:  # changed return type
        if not self.session_maker:
            self.session_maker = async_sessionmaker(  # changed
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
        return self.session_maker

    def default_engine(self):
        self.engine = create_async_engine(
            settings.database_uri,
            echo=True,
            future=True,
            connect_args=settings.db_context,
        )

    def refresh(self) -> None:
        self.default_engine()


async def get_session():
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
