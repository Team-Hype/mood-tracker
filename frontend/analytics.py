from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime

from models import (
    DailyAverage,
    MoodDistribution,
    MoodEntry,
    UserInsight,
    UserMoodSummary,
)

MOOD_LABELS: list[str] = ["Rough", "Low", "Okay", "Good", "Great"]

MOOD_SCORE: dict[str, int] = {label: i + 1 for i, label in enumerate(MOOD_LABELS)}

LOW_MOOD_THRESHOLD = 2


def _score(entry: MoodEntry) -> int:
    return MOOD_SCORE.get(entry.mood_entry, 3)


def build_distribution(entries: list[MoodEntry]) -> list[MoodDistribution]:
    counts: dict[str, int] = {label: 0 for label in MOOD_LABELS}
    for item in entries:
        if item.mood_entry in counts:
            counts[item.mood_entry] += 1
    return [
        MoodDistribution(mood_entry=label, count=counts[label]) for label in MOOD_LABELS
    ]


def build_daily_averages(entries: list[MoodEntry]) -> list[DailyAverage]:
    by_day: dict[date, list[int]] = defaultdict(list)
    for item in entries:
        day = (
            item.created_at.date()
            if isinstance(item.created_at, datetime)
            else date.fromisoformat(str(item.created_at))
        )
        by_day[day].append(_score(item))
    return [
        DailyAverage(day=d, average_mood=sum(scores) / len(scores))
        for d, scores in sorted(by_day.items())
    ]


def build_user_summaries(entries: list[MoodEntry]) -> list[UserMoodSummary]:
    by_user: dict[str, list[MoodEntry]] = defaultdict(list)
    for item in entries:
        by_user[item.username].append(item)

    summaries: list[UserMoodSummary] = []
    for username, user_entries in by_user.items():
        ordered = sorted(user_entries, key=lambda e: e.created_at)
        last = ordered[-1]
        avg = sum(_score(e) for e in ordered) / len(ordered)
        last_date = (
            last.created_at.strftime("%Y-%m-%d %H:%M")
            if isinstance(last.created_at, datetime)
            else str(last.created_at)
        )
        summaries.append(
            UserMoodSummary(
                username=username,
                average_mood=avg,
                last_mood_entry=last.mood_entry,
                last_mood_emoji=last.mood_emoji,
                entries_count=len(ordered),
                last_date=last_date,
                last_comment=last.comment,
            )
        )
    return sorted(summaries, key=lambda s: s.username.lower())


def build_insights(entries: list[MoodEntry]) -> list[UserInsight]:
    if not entries:
        return []

    insights: list[UserInsight] = []
    summaries = build_user_summaries(entries)

    for summary in summaries:
        last_score = MOOD_SCORE.get(summary.last_mood_entry, 3)
        if last_score <= LOW_MOOD_THRESHOLD:
            severity = "high" if last_score == 1 else "medium"
            insights.append(
                UserInsight(
                    username=summary.username,
                    headline=(
                        f"Latest mood is {summary.last_mood_entry} ({last_score}/5). "
                        "A short check-in or pairing might help this week."
                    ),
                    severity=severity,
                )
            )
        if summary.entries_count >= 3 and summary.average_mood < 3.0:
            insights.append(
                UserInsight(
                    username=summary.username,
                    headline=(
                        f"Rolling average is {summary.average_mood:.2f}/5 over "
                        f"{summary.entries_count} entries. Watch workload and blockers."
                    ),
                    severity="medium",
                )
            )

    return insights
