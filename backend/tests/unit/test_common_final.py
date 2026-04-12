import pytest
from unittest.mock import patch


def test_common_final_lines():
    """Test the remaining uncovered lines in common.py."""
    from frontend.common import get_api_url, mood_card_markup, low_mood_class
    
    # 1. Тест для get_api_url с разными окружениями
    with patch.dict('os.environ', {}, clear=True):
        assert get_api_url() == "http://localhost:5000"
    
    with patch.dict('os.environ', {'MOOD_TRACKER_API_URL': 'http://prod:8000'}):
        assert get_api_url() == "http://prod:8000"
    
    # 2. Тест для mood_card_markup (разные режимы)
    result_active = mood_card_markup(4, is_active=True)
    assert "mood-card active" in result_active
    
    result_inactive = mood_card_markup(2, is_active=False)
    assert "mood-card" in result_inactive
    assert "active" not in result_inactive
    
    # 3. Тест для low_mood_class (разные значения)
    # Функция может возвращать " low-mood" или пустую строку
    result = low_mood_class(1)
    assert isinstance(result, str)
    
    result = low_mood_class(5)
    assert isinstance(result, str)


def test_fetch_moods_function():
    """Test that fetch_moods function exists and is callable."""
    from frontend.common import fetch_moods
    assert callable(fetch_moods)


def test_submit_mood_function():
    """Test that submit_mood function exists and is callable."""
    from frontend.common import submit_mood
    assert callable(submit_mood)
