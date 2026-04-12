__all__ = ["lifespan"]

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db.connection.session import SessionManager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    sm = SessionManager()
    session_maker = sm.get_session_maker()

    try:
        async with session_maker() as session:
            await session.execute(text("SELECT 1"))
        logger.info("Database connection verified")
    except Exception as exc:
        logger.error("Database connection failed: %s", exc)

    yield

    await sm.engine.dispose()
