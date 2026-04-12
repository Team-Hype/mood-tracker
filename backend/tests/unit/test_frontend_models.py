import pytest
from datetime import datetime, date
from frontend.models import MoodEntry, MoodDistribution, DailyAverage, UserMoodSummary, UserInsight


class TestMoodEntry:
    def test_mood_entry_creation(self):
        """Test creating a MoodEntry."""
        entry = MoodEntry(
            id="1",
            username="alice",
            mood_entry="4",
            mood_emoji="🙂",
            comment="Good day",
            created_at=datetime.now()
        )
        assert entry.id == "1"
        assert entry.username == "alice"
        assert entry.mood_entry == "4"
        assert entry.mood_emoji == "🙂"
        assert entry.comment == "Good day"
    
    def test_mood_entry_immutability(self):
        """Test that MoodEntry is immutable."""
        entry = MoodEntry(
            id="1", 
            username="alice", 
            mood_entry="3", 
            mood_emoji="😐",
            comment="", 
            created_at=datetime.now()
        )
        with pytest.raises(Exception):
            entry.username = "bob"  # frozen=True, должно вызвать ошибку


class TestMoodDistribution:
    def test_mood_distribution_creation(self):
        """Test creating a MoodDistribution."""
        dist = MoodDistribution(mood_entry="3", count=5)
        assert dist.mood_entry == "3"
        assert dist.count == 5
    
    def test_mood_distribution_range(self):
        """Test mood in valid range."""
        for mood in range(1, 6):
            dist = MoodDistribution(mood_entry=str(mood), count=10)
            assert 1 <= int(dist.mood_entry) <= 5


class TestDailyAverage:
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
    def test_user_summary_creation(self):
        """Test creating a UserMoodSummary."""
        summary = UserMoodSummary(
            username="alice",
            average_mood=4.2,
            last_mood_entry="5",
            last_mood_emoji="😄",
            entries_count=10,
            last_date="2024-01-01",
            last_comment="Great!"
        )
        assert summary.username == "alice"
        assert summary.average_mood == 4.2
        assert summary.last_mood_entry == "5"
        assert summary.last_mood_emoji == "😄"
        assert summary.entries_count == 10
        assert summary.last_comment == "Great!"


class TestUserInsight:
    def test_user_insight_creation(self):
        """Test creating a UserInsight."""
        insight = UserInsight(
            username="bob",
            headline="Low mood detected",
            severity="high"
        )
        assert insight.username == "bob"
        assert insight.headline == "Low mood detected"
        assert insight.severity == "high"
