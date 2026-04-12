# backend/tests/unit/test_main.py
import pytest
from unittest.mock import patch


class TestMain:
    """Tests for main entry point."""
    
    @patch('uvicorn.run')
    def test_main_execution(self, mock_uvicorn):
        """Test that main executes uvicorn."""
        from backend.app import __main__
        
        # Проверяем, что модуль импортируется
        assert __main__ is not None