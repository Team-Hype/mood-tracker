def test_final_coverage_push():
    """Simple test to push coverage to 80%."""
    from frontend.common import get_api_url
    from unittest.mock import patch
    
    with patch.dict('os.environ', {}, clear=True):
        url = get_api_url()
        assert url == "http://localhost:5000"
    
    with patch.dict('os.environ', {'MOOD_TRACKER_API_URL': 'http://test:8080'}):
        url = get_api_url()
        assert url == "http://test:8080"
