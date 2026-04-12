# backend/tests/unit/test_common_coverage.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime


class TestCommonCoverage:
    """Tests to improve common.py coverage."""
    
    def test_get_api_url_default(self):
        """Test get_api_url returns default URL."""
        from frontend.common import get_api_url
        
        with patch.dict('os.environ', {}, clear=True):
            url = get_api_url()
            assert url == "http://localhost:5000"
    
    def test_get_api_url_from_env(self):
        """Test get_api_url returns env URL."""
        from frontend.common import get_api_url
        
        with patch.dict('os.environ', {'MOOD_TRACKER_API_URL': 'http://test:8000'}):
            url = get_api_url()
            assert url == "http://test:8000"
    
    def test_format_score(self):
        """Test format_score function."""
        from frontend.common import format_score
        
        assert format_score(4.0) == "4.00/5"
        assert format_score(3.333) == "3.33/5"
        assert format_score(2.5) == "2.50/5"
    
    def test_low_mood_class(self):
        """Test low_mood_class function."""
        from frontend.common import low_mood_class
        from frontend.analytics import LOW_MOOD_THRESHOLD
        
        assert low_mood_class(1) == " low-mood"
        assert low_mood_class(LOW_MOOD_THRESHOLD) == " low-mood"
        assert low_mood_class(LOW_MOOD_THRESHOLD + 1) == ""
    
    def test_mood_card_markup(self):
        """Test mood_card_markup function."""
        from frontend.common import mood_card_markup
        
        markup = mood_card_markup(mood=3, is_active=True)
        assert "mood-card active" in markup
        assert "Mood 3" in markup
        
        markup = mood_card_markup(mood=5, is_active=False)
        assert "mood-card" in markup
        assert "active" not in markup
    
    def test_coerce_datetime_with_string(self):
        """Test _coerce_datetime with string."""
        from frontend.common import _coerce_datetime
        
        result = _coerce_datetime("2024-01-01T12:00:00")
        assert isinstance(result, datetime)
    
    def test_coerce_datetime_with_datetime(self):
        """Test _coerce_datetime with datetime."""
        from frontend.common import _coerce_datetime
        
        now = datetime.now()
        result = _coerce_datetime(now)
        assert result == now