# frontend/common.py
"""Shared frontend helpers for Streamlit pages."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, TypedDict, cast

import requests

from .analytics import LOW_MOOD_THRESHOLD, MOOD_LABELS
from .models import MoodEntry

API_URL_ENV = "MOOD_TRACKER_API_URL"
DEFAULT_API_URL = "http://localhost:5000"
ACCENT_COLOR = "#F08CB2"
BACKGROUND_COLOR = "#1e1e1e"
SURFACE_COLOR = "#2a2a2a"
SURFACE_ALT = "#252525"
TEXT_COLOR = "#FFFFFF"
MUTED_TEXT = "#F7C6D9"
MOOD_EMOJIS = {1: "😡", 2: "😔", 3: "😐", 4: "🙂", 5: "😄"}


class MoodPayload(TypedDict):
    """Mood entry payload returned by the API."""

    id: str
    user: str
    mood: int
    mood_emoji: str
    mood_label: str
    comment: str | None
    date: str | datetime


def get_api_url() -> str:
    """Return the configured API base URL."""
    return os.getenv(API_URL_ENV, DEFAULT_API_URL).rstrip("/")


def fetch_moods() -> list[MoodPayload]:
    """Load mood entries from the backend."""
    response = requests.get(f"{get_api_url()}/moods", timeout=10.0)
    response.raise_for_status()
    moods = cast(list[dict[str, Any]], response.json())
    for item in moods:
        item["date"] = datetime.fromisoformat(str(item["date"]))
    return cast(list[MoodPayload], moods)


def submit_mood(user: str, mood: int, comment: str) -> None:
    """Submit a new mood entry to the backend."""
    response = requests.post(
        f"{get_api_url()}/moods",
        json={"user": user, "mood": mood, "comment": comment},
        timeout=10.0,
    )
    response.raise_for_status()


def to_domain_entries(raw_entries: list[MoodPayload]) -> list[MoodEntry]:
    """Convert API payloads into shared domain entries."""
    return [
        MoodEntry(
            id=str(item["id"]),
            user=str(item["user"]),
            mood=int(item["mood"]),
            comment=str(item.get("comment") or ""),
            date=_coerce_datetime(item["date"]),
        )
        for item in raw_entries
    ]


def global_styles() -> str:
    """Return shared CSS for the application."""
    return f"""
    <style>
    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(240, 140, 178, 0.20), transparent 30%),
            linear-gradient(180deg, #161616 0%, {BACKGROUND_COLOR} 100%);
        color: {TEXT_COLOR};
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, p, label {{
        color: {TEXT_COLOR};
    }}
    .hero-card, .metric-card, .insight-card {{
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1.25rem;
        border: 1px solid rgba(240, 140, 178, 0.18);
        background: linear-gradient(180deg, rgba(42, 42, 42, 0.96), rgba(30, 30, 30, 0.94));
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.24);
    }}
    .mood-card {{
        border-radius: 16px;
        padding: 0.9rem 0.7rem;
        min-height: 120px;
        border: 1px solid rgba(240, 140, 178, 0.14);
        background: {SURFACE_COLOR};
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    .mood-card.active {{
        border-color: {ACCENT_COLOR};
        background: {SURFACE_ALT};
        box-shadow: 0 0 0 1px rgba(240, 140, 178, 0.4), 0 12px 30px rgba(240, 140, 178, 0.25);
    }}
    .mood-card:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 30px rgba(240, 140, 178, 0.18);
    }}
    .mood-emoji {{
        font-size: 2rem;
        margin-bottom: 0.35rem;
    }}
    .mood-number {{
        font-size: 0.8rem;
        color: {MUTED_TEXT};
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }}
    .mood-label {{
        font-size: 0.95rem;
        font-weight: 600;
    }}
    .stButton > button {{
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(240, 140, 178, 0.25);
        background: transparent;
        color: {TEXT_COLOR};
        min-height: 130px;
        white-space: pre-line;
        font-size: 1rem;
        line-height: 1.5;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    .stButton > button:hover {{
        border-color: {ACCENT_COLOR};
        box-shadow: 0 0 24px rgba(240, 140, 178, 0.22);
        transform: translateY(-4px);
    }}
    .stAltairChart {{
        margin-top: 0.5rem;
    }}
    .stTextInput input, .stTextArea textarea {{
        border-radius: 14px;
        background: {SURFACE_COLOR};
        color: {TEXT_COLOR};
        border: 1px solid rgba(240, 140, 178, 0.18);
    }}
    .low-mood {{
        border-color: rgba(255, 108, 108, 0.8);
        box-shadow: 0 0 0 1px rgba(255, 108, 108, 0.4), 0 18px 45px rgba(255, 108, 108, 0.14);
    }}
    .caption {{
        color: {MUTED_TEXT};
    }}
    </style>
    """


def mood_card_markup(mood: int, is_active: bool) -> str:
    """Render card markup for a single mood selector item."""
    active_class = " active" if is_active else ""
    return f"""
    <div class="mood-card{active_class}">
        <div class="mood-emoji">{MOOD_EMOJIS[mood]}</div>
        <div class="mood-number">Mood {mood}</div>
        <div class="mood-label">{MOOD_LABELS[mood]}</div>
    </div>
    """


def format_score(score: float) -> str:
    """Format a mood score for display."""
    return f"{score:.2f}/5"


def low_mood_class(last_mood: int) -> str:
    """Return a CSS class for low-mood user cards."""
    return " low-mood" if last_mood <= LOW_MOOD_THRESHOLD else ""


def _coerce_datetime(value: str | datetime) -> datetime:
    """Convert a payload date value into a datetime."""
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)
