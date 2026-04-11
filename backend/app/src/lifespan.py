"""Application lifespan context manager for FastAPI startup and shutdown events."""

__all__ = ["lifespan"]

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db.connection.session import SessionManager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan: setup before yield, teardown after."""
    yield

    await sm.engine.dispose()
