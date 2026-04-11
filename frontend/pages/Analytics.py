"""Streamlit analytics page for mood insights."""

from __future__ import annotations

from typing import cast

import altair as alt
import pandas as pd
import streamlit as st

from frontend.analytics import (
    build_daily_averages,
    build_distribution,
    build_insights,
    build_user_summaries,
)
from frontend.common import (
    ACCENT_COLOR,
    BACKGROUND_COLOR,
    SURFACE_COLOR,
    fetch_moods,
    format_score,
    global_styles,
    low_mood_class,
    to_domain_entries,
)
from frontend.models import DailyAverage, MoodDistribution, UserInsight, UserMoodSummary


def main() -> None:
    """Render the analytics and insights dashboard."""
    st.set_page_config(page_title="Analytics", page_icon="💗", layout="wide")
    st.markdown(global_styles(), unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero-card">
            <h1>Analytics / Insights</h1>
            <p class="caption">
                Review distribution, trend lines, and user-level health before planning the
                next sprint.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        entries = to_domain_entries(fetch_moods())
    except Exception as exc:
        st.error(f"Could not load analytics data: {exc}")
        return

    if not entries:
        st.info("No mood entries yet. Submit the first update from the home page.")
        return

    distribution = build_distribution(entries)
    daily_averages = build_daily_averages(entries)
    summaries = build_user_summaries(entries)
    insights = build_insights(entries)

    _render_charts(distribution=distribution, daily_averages=daily_averages)
    _render_user_cards(summaries=summaries)
    _render_insights(insights=insights)


def _render_charts(
    *,
    distribution: list[MoodDistribution],
    daily_averages: list[DailyAverage],
) -> None:
    """Render the main analytics charts."""
    left_column, right_column = st.columns(2, gap="large")

    with left_column:
        st.altair_chart(_build_distribution_chart(distribution), width="stretch")
    with right_column:
        st.altair_chart(_build_daily_average_chart(daily_averages), width="stretch")


def _render_user_cards(*, summaries: list[UserMoodSummary]) -> None:
    """Render per-user statistic cards."""
    st.subheader("Users")
    for summary in summaries:
        st.markdown(
            f"""
            <div class="metric-card{low_mood_class(summary.last_mood)}">
                <h3>{summary.user}</h3>
                <p><strong>Average mood:</strong> {format_score(summary.average_mood)}</p>
                <p><strong>Latest mood:</strong> {summary.last_mood}/5</p>
                <p><strong>Entries:</strong> {summary.entries_count}</p>
                <p><strong>Last update:</strong> {summary.last_date}</p>
                <p class="caption">{summary.last_comment}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_insights(*, insights: list[UserInsight]) -> None:
    """Render rule-based textual insight cards."""
    st.subheader("Insights")
    for insight in insights:
        st.markdown(
            f"""
            <div class="insight-card">
                <p><strong>{insight.user}</strong></p>
                <p>{insight.headline}</p>
                <p class="caption">Severity: {insight.severity}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _build_distribution_chart(distribution: list[MoodDistribution]) -> alt.Chart:
    """Build the styled mood distribution bar chart."""
    distribution_frame = pd.DataFrame(
        {
            "Mood": [item.mood for item in distribution],
            "Entries": [item.count for item in distribution],
        }
    )
    return cast(
        alt.Chart,
        alt.Chart(distribution_frame)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color=ACCENT_COLOR)
        .encode(
            x=alt.X("Mood:O", title="Mood"),
            y=alt.Y("Entries:Q", title="Entries"),
            tooltip=["Mood", "Entries"],
        )
        .properties(title="Mood Distribution", height=320)
        .configure_view(strokeOpacity=0, fill=SURFACE_COLOR)
        .configure(background=BACKGROUND_COLOR)
        .configure_axis(labelColor="white", titleColor="white", gridColor="#3a3a3a")
        .configure_title(color="white"),
    )


def _build_daily_average_chart(daily_averages: list[DailyAverage]) -> alt.Chart:
    """Build the styled daily average line chart."""
    daily_frame = pd.DataFrame(
        {
            "Date": [item.day for item in daily_averages],
            "Average mood": [item.average_mood for item in daily_averages],
        }
    )
    return cast(
        alt.Chart,
        alt.Chart(daily_frame)
        .mark_line(
            point=alt.OverlayMarkDef(color=ACCENT_COLOR, filled=True),
            color=ACCENT_COLOR,
        )
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y(
                "Average mood:Q", title="Average mood", scale=alt.Scale(domain=[1, 5])
            ),
            tooltip=["Date", "Average mood"],
        )
        .properties(title="Average Mood by Day", height=320)
        .configure_view(strokeOpacity=0, fill=SURFACE_COLOR)
        .configure(background=BACKGROUND_COLOR)
        .configure_axis(labelColor="white", titleColor="white", gridColor="#3a3a3a")
        .configure_title(color="white"),
    )


if __name__ == "__main__":
    main()
