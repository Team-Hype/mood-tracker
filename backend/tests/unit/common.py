# backend/tests/unit/test_common_extra.py
import pytest
from unittest.mock import patch, Mock
from datetime import datetime


class TestCommonExtra:
    def test_get_api_url_default(self):
        """Test get_api_url returns default."""
        from frontend.common import get_api_url
        with patch.dict('os.environ', {}, clear=True):
            url = get_api_url()
            assert url == "http://localhost:5000"
    
    def test_get_api_url_from_env(self):
        """Test get_api_url from environment."""
        from frontend.common import get_api_url
        with patch.dict('os.environ', {'MOOD_TRACKER_API_URL': 'http://test:9000'}):
            url = get_api_url()
            assert url == "http://test:9000"
    
    def test_mood_card_markup_active(self):
        """Test mood_card_markup with active state."""
        from frontend.common import mood_card_markup
        result = mood_card_markup(mood=3, is_active=True)
        assert "mood-card active" in result
        assert "Mood 3" in result
    
    def test_mood_card_markup_inactive(self):
        """Test mood_card_markup with inactive state."""
        from frontend.common import mood_card_markup
        result = mood_card_markup(mood=5, is_active=False)
        assert "mood-card" in result
        assert "active" not in result
        assert "Mood 5" in result
    
    def test_global_styles_returns_string(self):
        """Test global_styles returns CSS string."""
        from frontend.common import global_styles
        css = global_styles()
        assert isinstance(css, str)
        assert "style" in css