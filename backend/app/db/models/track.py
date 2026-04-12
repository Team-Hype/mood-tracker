"""Database model for mood tracking entries."""

from datetime import datetime

from sqlalchemy import Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.mixins.index import UUIDMixin
from .. import DeclarativeBase as Base


class MoodTrack(UUIDMixin, Base):
    """Represents a user's mood tracking record."""

    __tablename__ = "mood_track"

    username: Mapped[str] = mapped_column(
        nullable=False, comment="Username of the entry author"
    )
    mood_entry: Mapped[str] = mapped_column(
        nullable=False, comment="Mood entry description"
    )
    mood_emoji: Mapped[str] = mapped_column(
        nullable=False, comment="Mood emoji representation"
    )
    comment: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Optional user comment"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Date and time of the entry creation",
    )
