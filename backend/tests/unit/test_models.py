# backend/tests/unit/test_models.py
import pytest
from datetime import datetime
from app.db.models.track import MoodTrack


class TestMoodTrackModel:
    """Tests for MoodTrack model."""
    
    def test_moodtrack_creation(self):
        """Test creating a MoodTrack instance."""
        track = MoodTrack(
            username="test_user",
            mood_entry=4,
            comment="Feeling good",
            created_at=datetime.now()
        )
        
        assert track.username == "test_user"
        assert track.mood_entry == 4
        assert track.comment == "Feeling good"
        assert track.created_at is not None
    
    def test_moodtrack_mood_range(self):
        """Test mood values in range 1-5."""
        for mood in range(1, 6):
            track = MoodTrack(
                username="user",
                mood_entry=mood,
                comment="test",
                created_at=datetime.now()
            )
            assert 1 <= track.mood_entry <= 5
    
    def test_moodtrack_optional_comment(self):
        """Test that comment can be optional."""
        track = MoodTrack(
            username="user",
            mood_entry=3,
            comment=None,
            created_at=datetime.now()
        )
        assert track.comment is None
    
    def test_moodtrack_created_at_auto(self):
        """Test that created_at can be set manually."""
        # В SQLAlchemy created_at не auto-generated в памяти,
        # поэтому мы устанавливаем его явно для теста
        now = datetime.now()
        track = MoodTrack(
            username="user",
            mood_entry=3,
            comment="test",
            created_at=now
        )
        assert track.created_at is not None
        assert track.created_at == now
        assert isinstance(track.created_at, datetime)
    
    def test_moodtrack_created_at_without_value(self):
        """Test that created_at can be None when not provided."""
        track = MoodTrack(
            username="user",
            mood_entry=3,
            comment="test"
        )
        # Если не передали, то created_at будет None (в памяти)
        # База данных установит auto-generated значение при сохранении
        assert track.created_at is None
    
    # backend/tests/unit/test_models.py
