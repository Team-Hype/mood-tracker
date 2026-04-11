"""Application lifespan context manager for FastAPI startup and shutdown events."""

__all__ = ["lifespan"]
from fastapi import FastAPI


async def lifespan(app: FastAPI):
    """Manage application lifespan: setup before yield, teardown after."""
    yield
