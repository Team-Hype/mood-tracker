from __future__ import annotations

from typing import cast

import altair as alt
import pandas as pd
import streamlit as st

from frontend.analytics import (
    MOOD_LABELS,
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
    left, right = st.columns(2, gap="large")
    with left:
        st.altair_chart(_distribution_chart(distribution), use_container_width=True)
    with right:
        st.altair_chart(_daily_chart(daily_averages), use_container_width=True)


def _render_user_cards(*, summaries: list[UserMoodSummary]) -> None:
    st.subheader("Users")
    if not summaries:
        st.info("No user data to display.")
        return
    for s in summaries:
        comment_html = f'<p class="caption">{s.last_comment}</p>' if s.last_comment else ""
        st.markdown(
            f"""
            <div class="metric-card{low_mood_class(s.last_mood_entry)}">
                <h3>{s.username}</h3>
                <p><strong>Average mood:</strong> {format_score(s.average_mood)}</p>
                <p><strong>Latest:</strong> {s.last_mood_emoji} {s.last_mood_entry}</p>
                <p><strong>Entries:</strong> {s.entries_count}</p>
                <p><strong>Last update:</strong> {s.last_date}</p>
                {comment_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_insights(*, insights: list[UserInsight]) -> None:
    st.subheader("Insights")
    if not insights:
        st.success("All good — no concerns detected across the team.")
        return
    for insight in insights:
        st.markdown(
            f"""
            <div class="insight-card">
                <p><strong>{insight.username}</strong></p>
                <p>{insight.headline}</p>
                <p class="caption">Severity: {insight.severity}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _distribution_chart(distribution: list[MoodDistribution]) -> alt.Chart:
    df = pd.DataFrame(
        {
            "Mood": [d.mood_entry for d in distribution],
            "Entries": [d.count for d in distribution],
        }
    )
    return cast(
        alt.Chart,
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color=ACCENT_COLOR)
        .encode(
            x=alt.X("Mood:N", title="Mood", sort=MOOD_LABELS),
            y=alt.Y("Entries:Q", title="Entries"),
            tooltip=["Mood", "Entries"],
        )
        .properties(title="Mood Distribution", height=320)
        .configure_view(strokeOpacity=0, fill=SURFACE_COLOR)
        .configure(background=BACKGROUND_COLOR)
        .configure_axis(labelColor="white", titleColor="white", gridColor="#3a3a3a")
        .configure_title(color="white"),
    )


def _daily_chart(daily_averages: list[DailyAverage]) -> alt.Chart:
    daily_frame = pd.DataFrame(
        {
            "Date": [d.day for d in daily_averages],
            "Average mood": [d.average_mood for d in daily_averages],
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
            y=alt.Y("Average mood:Q", title="Average mood", scale=alt.Scale(domain=[1, 5])),
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
