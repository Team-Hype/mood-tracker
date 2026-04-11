"""Domain types for the Streamlit mood UI."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class MoodEntry:
    """Single mood check-in from the API or store."""

    id: int
    user: str
    mood: int
    comment: str
    date: datetime


@dataclass(frozen=True, slots=True)
class MoodDistribution:
    """Count of entries for one mood score."""

    mood: int
    count: int


@dataclass(frozen=True, slots=True)
class DailyAverage:
    """Average mood for a calendar day."""

    day: date
    average_mood: float


@dataclass(frozen=True, slots=True)
class UserMoodSummary:
    """Aggregated stats for one user."""

    user: str
    average_mood: float
    last_mood: int
    entries_count: int
    last_date: str
    last_comment: str


@dataclass(frozen=True, slots=True)
class UserInsight:
    """Rule-based insight for display on the analytics page."""

    user: str
    headline: str
    severity: str
