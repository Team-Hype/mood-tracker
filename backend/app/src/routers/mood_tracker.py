"""Mood tracking endpoints – create, retrieve, list, and delete mood entries."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import SessionDependency
from app.db.models.track import MoodTrack

router = APIRouter(prefix="/moods", tags=["Moods"])

MOOD_EMOJIS: dict[str, str] = {
    "Rough": "😡",
    "Low": "😔",
    "Okay": "😐",
    "Good": "🙂",
    "Great": "😄",
}

VALID_MOOD_ENTRIES = list(MOOD_EMOJIS.keys())


class MoodCreateRequest(BaseModel):
    """Request body for creating a new mood entry."""

    username: str = Field(..., min_length=1, max_length=50, examples=["Anna"])
    mood_entry: str = Field(
        ...,
        description="One of: Rough, Low, Okay, Good, Great",
        examples=["Good"],
    )
    comment: str | None = Field(
        None,
        max_length=500,
        examples=["Had a productive day"],
    )


class MoodResponse(BaseModel):
    """Response schema for a mood entry, including computed emoji and timestamp."""

    id: UUID
    username: str
    mood_entry: str
    mood_emoji: str
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


async def _create_mood(
    session: AsyncSession,
    *,
    username: str,
    mood_entry: str,
    comment: str | None,
) -> MoodTrack:
    """Create a new mood entry in the database and return the ORM object."""
    entry = MoodTrack(
        username=username,
        mood_entry=mood_entry,
        mood_emoji=MOOD_EMOJIS[mood_entry],
        comment=comment,
    )
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


async def _list_moods(
    session: AsyncSession,
    *,
    username: str | None = None,
    limit: int = 500,
    offset: int = 0,
) -> list[MoodTrack]:
    """Return a list of mood entries, optionally filtered by username."""
    query = select(MoodTrack)
    if username:
        query = query.where(MoodTrack.username == username)
    query = query.order_by(MoodTrack.created_at.desc()).limit(limit).offset(offset)
    result = await session.execute(query)
    return list(result.scalars().all())


async def _get_mood(session: AsyncSession, mood_id: UUID) -> MoodTrack | None:
    """Retrieve a single mood entry by its UUID, or None if not found."""
    return await session.get(MoodTrack, mood_id)


async def _delete_mood(session: AsyncSession, mood_id: UUID) -> bool:
    """Delete a mood entry by UUID. Returns True if deleted, False if not found."""
    entry = await _get_mood(session, mood_id)
    if entry is None:
        return False
    await session.delete(entry)
    await session.commit()
    return True


@router.get("", response_model=list[MoodResponse])
async def get_moods(
    session: SessionDependency,
    username: str | None = Query(None),
    limit: int = Query(500, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Retrieve all mood entries, with optional filtering by username and pagination."""
    return await _list_moods(session, username=username, limit=limit, offset=offset)


@router.get("/{mood_id}", response_model=MoodResponse)
async def get_mood(mood_id: UUID, session: SessionDependency):
    """Fetch a single mood entry by its ID. Returns 404 if not found."""
    entry = await _get_mood(session, mood_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return entry


@router.post("", response_model=MoodResponse, status_code=201)
async def post_mood(body: MoodCreateRequest, session: SessionDependency):
    """Create a new mood entry. Validates mood_entry against allowed values."""
    if body.mood_entry not in VALID_MOOD_ENTRIES:
        raise HTTPException(
            status_code=422,
            detail=f"mood_entry must be one of: {', '.join(VALID_MOOD_ENTRIES)}",
        )
    return await _create_mood(
        session,
        username=body.username,
        mood_entry=body.mood_entry,
        comment=body.comment,
    )


@router.delete("/{mood_id}", status_code=204)
async def remove_mood(mood_id: UUID, session: SessionDependency):
    """Delete a mood entry by ID. Returns 204 on success, 404 if not found."""
    if not await _delete_mood(session, mood_id):
        raise HTTPException(status_code=404, detail="Mood entry not found")
