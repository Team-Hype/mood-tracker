# backend/tests/unit/test_analytics.py
import pytest
from datetime import datetime, timedelta, date
from frontend.analytics import (
    build_distribution,
    build_daily_averages,
    build_user_summaries,
    build_insights,
    LOW_MOOD_THRESHOLD
)
from frontend.models import MoodEntry


class TestAnalytics:
    """Tests for analytics functions."""
    
    @pytest.fixture
    def sample_entries(self):
        """Create sample mood entries for testing."""
        base_date = datetime.now()
        return [
            MoodEntry(id=1, user="alice", mood=5, comment="Great!", date=base_date),
            MoodEntry(id=2, user="alice", mood=4, comment="Good", date=base_date - timedelta(days=1)),
            MoodEntry(id=3, user="bob", mood=2, comment="Bad", date=base_date),
            MoodEntry(id=4, user="bob", mood=3, comment="Okay", date=base_date - timedelta(days=1)),
            MoodEntry(id=5, user="charlie", mood=1, comment="Terrible", date=base_date),
        ]
    
    def test_build_distribution(self, sample_entries):
        """Test building mood distribution."""
        distribution = build_distribution(sample_entries)
        
        assert len(distribution) == 5  # Moods 1-5
        # Проверяем counts
        counts = {d.mood: d.count for d in distribution}
        assert counts[5] == 1  # alice's 5
        assert counts[4] == 1  # alice's 4
        assert counts[2] == 1  # bob's 2
        assert counts[3] == 1  # bob's 3
        assert counts[1] == 1  # charlie's 1
    
    def test_build_distribution_empty(self):
        """Test building distribution with empty list."""
        distribution = build_distribution([])
        assert len(distribution) == 5
        for d in distribution:
            assert d.count == 0
    
    def test_build_daily_averages(self, sample_entries):
        """Test building daily averages."""
        averages = build_daily_averages(sample_entries)
        assert len(averages) > 0
        for avg in averages:
            assert 1.0 <= avg.average_mood <= 5.0
    
    def test_build_user_summaries(self, sample_entries):
        """Test building user summaries."""
        summaries = build_user_summaries(sample_entries)
        
        assert len(summaries) == 3  # alice, bob, charlie
        
        # Проверяем alice
        alice = next(s for s in summaries if s.user == "alice")
        assert alice.entries_count == 2
        assert alice.average_mood == 4.5  # (5+4)/2
        assert alice.last_mood == 5
    
    def test_build_insights_low_mood(self, sample_entries):
        """Test building insights for low mood."""
        insights = build_insights(sample_entries)
        
        # Должны быть инсайты для bob (mood=2) и charlie (mood=1)
        low_mood_users = [i.user for i in insights if "Latest mood" in i.headline]
        assert "bob" in low_mood_users or "charlie" in low_mood_users
    
    def test_build_insights_average_low(self):
        """Test insights for consistently low average mood."""
        base_date = datetime.now()
        entries = [
            MoodEntry(id=i, user="dave", mood=2, comment="", date=base_date - timedelta(days=i))
            for i in range(3)
        ]
        insights = build_insights(entries)
        
        # Должен быть инсайт о низком среднем
        avg_insights = [i for i in insights if "Rolling average" in i.headline]
        assert len(avg_insights) > 0
    
    def test_build_insights_empty(self):
        """Test building insights with empty list."""
        insights = build_insights([])
        assert insights == []