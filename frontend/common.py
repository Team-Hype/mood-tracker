from __future__ import annotations

import os
from datetime import datetime
from typing import Any, cast

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

MOOD_EMOJIS: dict[str, str] = {
    "Rough": "😡",
    "Low": "😔",
    "Okay": "😐",
    "Good": "🙂",
    "Great": "😄",
}


def get_api_url() -> str:
    return os.getenv(API_URL_ENV, DEFAULT_API_URL).rstrip("/")


def fetch_moods() -> list[MoodPayload]:
    """Load mood entries from the backend."""
    response = requests.get(f"{get_api_url()}/moods", timeout=10.0)
    response.raise_for_status()
    return cast(list[dict[str, Any]], response.json())


def submit_mood(user: str, mood: int, comment: str) -> None:
    """Submit a new mood entry to the backend."""
    response = requests.post(
        f"{get_api_url()}/moods",
        json={"username": username, "mood_entry": mood_entry, "comment": comment},
        timeout=10.0,
    )
    response.raise_for_status()


def to_domain_entries(raw: list[dict[str, Any]]) -> list[MoodEntry]:
    return [
        MoodEntry(
            id=str(item["id"]),
            username=str(item["username"]),
            mood_entry=str(item["mood_entry"]),
            mood_emoji=str(item["mood_emoji"]),
            comment=item.get("comment"),
            created_at=_coerce_datetime(item["created_at"]),
        )
        for item in raw
    ]


def _coerce_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def format_score(score: float) -> str:
    return f"{score:.2f}/5"


def low_mood_class(mood_entry: str) -> str:
    return " low-mood" if MOOD_SCORE.get(mood_entry, 3) <= 2 else ""


def mood_card_markup(mood_label: str, is_active: bool) -> str:
    emoji = MOOD_EMOJIS.get(mood_label, "❓")
    active_class = " active" if is_active else ""
    return f"""
    <div class="mood-card{active_class}">
        <div class="mood-emoji">{emoji}</div>
        <div class="mood-label">{mood_label}</div>
    </div>
    """


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
        min-height: 120px;
        border-radius: 16px;
        background: {SURFACE_COLOR};
        border: 1px solid rgba(240, 140, 178, 0.14);
        color: {TEXT_COLOR};
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
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
