# backend/tests/unit/test_home_mock.py
import pytest
from unittest.mock import patch, MagicMock
import sys

# Мокаем streamlit для всех тестов
mock_st = MagicMock()
sys.modules['streamlit'] = mock_st


class TestHomeWithMock:
    def test_mood_labels_import(self):
        """Test that Home can be imported with mocked streamlit."""
        # Мокаем зависимости
        with patch.dict('sys.modules', {
            'streamlit': mock_st,
            'common': MagicMock(),
            'analytics': MagicMock()
        }):
            from frontend import Home
            assert hasattr(Home, 'main')
    
    def test_mood_range_exists(self):
        """Test that MOOD_LABELS is accessible."""
        from frontend.analytics import MOOD_LABELS
        assert len(MOOD_LABELS) == 5
        assert MOOD_LABELS[0] == "Rough"
        assert MOOD_LABELS[4] == "Great"