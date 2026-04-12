from app.db.models.track import MoodTrack


def test_table_name():
    assert MoodTrack.__tablename__ == "mood_track"