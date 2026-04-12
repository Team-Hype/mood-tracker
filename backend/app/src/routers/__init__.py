"""Router aggregation for the Mood Tracker API."""

__all__ = ["router"]

from fastapi import APIRouter

from .mood_tracker import router as mood_router

router = APIRouter()
router.include_router(mood_router)
