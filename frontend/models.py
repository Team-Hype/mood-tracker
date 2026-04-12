from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True, slots=True)
class MoodEntry:
    id: str
    username: str
    mood_entry: str
    mood_emoji: str
    comment: str | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class MoodDistribution:
    mood_entry: str
    count: int


@dataclass(frozen=True, slots=True)
class DailyAverage:
    day: date
    average_mood: float


@dataclass(frozen=True, slots=True)
class UserMoodSummary:
    username: str
    average_mood: float
    last_mood_entry: str
    last_mood_emoji: str
    entries_count: int
    last_date: str
    last_comment: str | None


@dataclass(frozen=True, slots=True)
class UserInsight:
    username: str
    headline: str
    severity: str
