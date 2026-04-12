# backend/tests/unit/test_frontend_models.py
import pytest
from datetime import datetime, date
from frontend.models import (
    MoodEntry, MoodDistribution, DailyAverage, 
    UserMoodSummary, UserInsight
)


class TestMoodEntry:
    """Tests for MoodEntry model."""
    
    def test_mood_entry_creation(self):
        """Test creating a MoodEntry."""
        entry = MoodEntry(
            id=1,
            user="alice",
            mood=4,
            comment="Good day",
            date=datetime.now()
        )
        assert entry.id == 1
        assert entry.user == "alice"
        assert entry.mood == 4
        assert entry.comment == "Good day"
    
    def test_mood_entry_immutability(self):
        """Test that MoodEntry is immutable (frozen)."""
        entry = MoodEntry(id=1, user="alice", mood=3, comment="", date=datetime.now())
        with pytest.raises(Exception):
            entry.user = "bob"  # Should raise error if frozen


class TestMoodDistribution:
    """Tests for MoodDistribution model."""
    
    def test_mood_distribution_creation(self):
        """Test creating a MoodDistribution."""
        dist = MoodDistribution(mood=3, count=5)
        assert dist.mood == 3
        assert dist.count == 5
    
    def test_mood_distribution_range(self):
        """Test mood in valid range."""
        for mood in range(1, 6):
            dist = MoodDistribution(mood=mood, count=10)
            assert 1 <= dist.mood <= 5


class TestDailyAverage:
    """Tests for DailyAverage model."""
    
    def test_daily_average_creation(self):
        """Test creating a DailyAverage."""
        today = date.today()
        avg = DailyAverage(day=today, average_mood=3.5)
        assert avg.day == today
        assert avg.average_mood == 3.5
    
    def test_daily_average_mood_range(self):
        """Test average mood in valid range."""
        avg = DailyAverage(day=date.today(), average_mood=2.5)
        assert 1.0 <= avg.average_mood <= 5.0


class TestUserMoodSummary:
    """Tests for UserMoodSummary model."""
    
    def test_user_summary_creation(self):
        """Test creating a UserMoodSummary."""
        summary = UserMoodSummary(
            user="alice",
            average_mood=4.2,
            last_mood=5,
            entries_count=10,
            last_date="2024-01-01",
            last_comment="Great!"
        )
        assert summary.user == "alice"
        assert summary.average_mood == 4.2
        assert summary.last_mood == 5
        assert summary.entries_count == 10


class TestUserInsight:
    """Tests for UserInsight model."""
    
    def test_user_insight_creation(self):
        """Test creating a UserInsight."""
        insight = UserInsight(
            user="bob",
            headline="Low mood detected",
            severity="high"
        )
        assert insight.user == "bob"
        assert insight.headline == "Low mood detected"
        assert insight.severity in ["low", "medium", "high"]