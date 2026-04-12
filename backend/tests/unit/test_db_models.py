import pytest
from datetime import datetime

from app.db.models.track import MoodTrack


def test_moodtrack_fields_exist():
    assert hasattr(MoodTrack, "username")
    assert hasattr(MoodTrack, "mood_entry")
    assert hasattr(MoodTrack, "comment")
    assert hasattr(MoodTrack, "created_at")