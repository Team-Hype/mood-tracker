import pytest
from unittest.mock import patch


class TestCommonQuick:
    def test_get_api_url_default(self):
        from frontend.common import get_api_url
        with patch.dict('os.environ', {}, clear=True):
            assert get_api_url() == "http://localhost:5000"
    
    def test_get_api_url_from_env(self):
        from frontend.common import get_api_url
        with patch.dict('os.environ', {'MOOD_TRACKER_API_URL': 'http://test:9000'}):
            assert get_api_url() == "http://test:9000"
    
    def test_mood_card_markup(self):
        from frontend.common import mood_card_markup
        result = mood_card_markup(3, True)
        assert "mood-card active" in result
    
    def test_global_styles_returns_string(self):
        from frontend.common import global_styles
        css = global_styles()
        assert isinstance(css, str)
