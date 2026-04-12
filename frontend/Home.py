import streamlit as st

from frontend.common import global_styles, mood_card_markup, submit_mood

MOOD_RANGE = [1, 2, 3, 4, 5]


def main() -> None:
    st.set_page_config(page_title="Mood Tracker", page_icon="💗", layout="wide")
    st.markdown(global_styles(), unsafe_allow_html=True)

    if "selected_mood" not in st.session_state:
        st.session_state["selected_mood"] = "Okay"

    st.markdown(
        """
        <div class="hero-card">
            <h1>Team Mood Tracker</h1>
            <p class="caption">
                Capture team sentiment in a clean, product-style flow and keep the pulse visible.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    _render_mood_selector()

    with st.form("mood-form", clear_on_submit=True):
        username = st.text_input("User name", max_chars=50, placeholder="Anna")
        comment = st.text_area(
            "Comment",
            max_chars=500,
            placeholder="Share context, blockers, or wins.",
            height=140,
        )
        submitted = st.form_submit_button("Submit")

        if submitted:
            _handle_submit(
                user=username,
                comment=comment,
                mood=int(st.session_state["selected_mood"]),
            )

    st.caption(f"Selected mood: {st.session_state['selected_mood']}")


def _render_mood_selector() -> None:
    st.subheader("How are you feeling?")
    columns = st.columns(5, gap="medium")
    for mood, column in zip(MOOD_RANGE, columns, strict=True):
        with column:
            st.markdown(
                mood_card_markup(mood=mood, is_active=st.session_state["selected_mood"] == mood),
                unsafe_allow_html=True,
            )
            if st.button(f"Choose {mood}", key=f"mood-{mood}", width="stretch"):
                st.session_state["selected_mood"] = mood
                st.rerun()


def _handle_submit(username: str, comment: str, mood_entry: str) -> None:
    trimmed_user = username.strip()
    trimmed_comment = comment.strip()

    if not trimmed_user:
        st.error("Please enter a user name before submitting.")
        return
    if not trimmed_comment:
        st.error("Please add a short comment to give the mood some context.")
        return

    try:
        submit_mood(
            username=trimmed_user,
            mood_entry=mood_entry,
            comment=trimmed_comment,
        )
    except Exception as exc:
        st.error(f"Could not submit the mood entry: {exc}")
        return

    st.success("Mood submitted successfully. Head to Analytics for the latest insights.")


if __name__ == "__main__":
    main()
