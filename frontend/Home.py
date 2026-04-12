import streamlit as st

from common import MOOD_EMOJIS, global_styles, submit_mood
from analytics import MOOD_LABELS


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
                username=username,
                comment=comment,
                mood_entry=st.session_state["selected_mood"],
            )

    st.caption(f"Selected mood: {st.session_state['selected_mood']}")


def _render_mood_selector() -> None:
    st.subheader("How are you feeling?")
    cols = st.columns(len(MOOD_LABELS), gap="medium")

    for label, col in zip(MOOD_LABELS, cols, strict=True):
        with col:
            # Build button label with emoji + label
            emoji = MOOD_EMOJIS.get(label, "❓")
            button_label = f"{emoji}\n\n{label}"

            # Use a button styled like the mood card
            if st.button(
                button_label,
                key=f"mood_btn_{label}",
                use_container_width=True,
            ):
                st.session_state["selected_mood"] = label
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

    st.success("Mood submitted! Head to Analytics for the latest insights.")


if __name__ == "__main__":
    main()
