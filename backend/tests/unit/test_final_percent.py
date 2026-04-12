import pytest
from unittest.mock import patch


def test_get_api_url_coverage():
    """Test get_api_url to cover the last missing lines."""
    from frontend.common import get_api_url
    
    # Тест для покрытия default URL
    with patch.dict('os.environ', {}, clear=True):
        url = get_api_url()
        assert url == "http://localhost:5000"
    
    # Тест для покрытия URL из окружения
    with patch.dict('os.environ', {'MOOD_TRACKER_API_URL': 'http://test:8000'}):
        url = get_api_url()
        assert url == "http://test:8000"
