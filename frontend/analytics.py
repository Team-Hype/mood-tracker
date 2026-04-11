"""Analytics helpers shared by Streamlit pages."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from .models import (
    DailyAverage,
    MoodDistribution,
    MoodEntry,
    UserInsight,
    UserMoodSummary,
)

MOOD_LABELS: dict[int, str] = {
    1: "Rough",
    2: "Low",
    3: "Okay",
    4: "Good",
    5: "Great",
}

LOW_MOOD_THRESHOLD = 2


def build_distribution(entries: list[MoodEntry]) -> list[MoodDistribution]:
    """Return entry counts for moods 1–5."""
    counts = {m: 0 for m in range(1, 6)}
    for item in entries:
        if 1 <= item.mood <= 5:
            counts[item.mood] += 1
    return [MoodDistribution(mood=m, count=counts[m]) for m in range(1, 6)]


def build_daily_averages(entries: list[MoodEntry]) -> list[DailyAverage]:
    """Average mood per calendar day."""
    by_day: dict[date, list[int]] = defaultdict(list)
    for item in entries:
        day = (
            item.date.date()
            if isinstance(item.date, datetime)
            else date.fromisoformat(str(item.date))
        )
        by_day[day].append(item.mood)
    return [
        DailyAverage(day=d, average_mood=sum(moods) / len(moods))
        for d, moods in sorted(by_day.items(), key=lambda pair: pair[0])
    ]


def build_user_summaries(entries: list[MoodEntry]) -> list[UserMoodSummary]:
    """Per-user aggregates, sorted by name."""
    by_user: dict[str, list[MoodEntry]] = defaultdict(list)
    for item in entries:
        by_user[item.user].append(item)

    summaries: list[UserMoodSummary] = []
    for user, user_entries in by_user.items():
        ordered = sorted(user_entries, key=lambda e: e.date)
        last = ordered[-1]
        avg = sum(e.mood for e in ordered) / len(ordered)
        last_dt = last.date
        last_date = (
            last_dt.strftime("%Y-%m-%d %H:%M")
            if isinstance(last_dt, datetime)
            else str(last_dt)
        )
        summaries.append(
            UserMoodSummary(
                user=user,
                average_mood=avg,
                last_mood=last.mood,
                entries_count=len(ordered),
                last_date=last_date,
                last_comment=last.comment,
            )
        )
    return sorted(summaries, key=lambda s: s.user.lower())


def build_insights(entries: list[MoodEntry]) -> list[UserInsight]:
    """Lightweight rule-based insights from recent patterns."""
    if not entries:
        return []

    insights: list[UserInsight] = []
    summaries = build_user_summaries(entries)

    for summary in summaries:
        if summary.last_mood <= LOW_MOOD_THRESHOLD:
            severity = "high" if summary.last_mood == 1 else "medium"
            insights.append(
                UserInsight(
                    user=summary.user,
                    headline=(
                        f"Latest mood is {summary.last_mood}/5. "
                        "A short check-in or pairing might help this week."
                    ),
                    severity=severity,
                )
            )
        if summary.entries_count >= 3 and summary.average_mood < 3.0:
            insights.append(
                UserInsight(
                    user=summary.user,
                    headline=(
                        f"Rolling average is {summary.average_mood:.2f}/5 over "
                        f"{summary.entries_count} entries. Watch workload and blockers."
                    ),
                    severity="medium",
                )
            )

    return insights
