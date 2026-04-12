# backend/tests/unit/test_settings.py
import pytest
from app.src.settings import settings


class TestSettings:
    """Tests for application settings."""
    
    def test_settings_have_required_attributes(self):
        """Test that settings have all required attributes."""
        assert hasattr(settings, "APP_NAME")
        assert hasattr(settings, "PATH_PREFIX")
        assert hasattr(settings, "APP_HOST")
        assert hasattr(settings, "APP_PORT")
        assert hasattr(settings, "POSTGRES_DB")
        assert hasattr(settings, "POSTGRES_HOST")
        assert hasattr(settings, "POSTGRES_USER")
    
    def test_database_uri_returns_string(self):
        """Test that database_uri returns a string."""
        uri = settings.database_uri
        assert isinstance(uri, str)
        assert "postgresql+asyncpg://" in uri
    
    def test_database_uri_sync_returns_string(self):
        """Test that database_uri_sync returns a string."""
        uri = settings.database_uri_sync
        assert isinstance(uri, str)
        assert "postgresql://" in uri
        assert "asyncpg" not in uri
    
    def test_current_host_url_format(self):
        """Test that current_host_url has correct format."""
        url = settings.current_host_url
        assert isinstance(url, str)
        assert url.startswith(("http://", "https://"))
    
    def test_database_settings_returns_dict(self):
        """Test that database_settings returns a dictionary."""
        db_settings = settings.database_settings
        assert isinstance(db_settings, dict)
        assert "database" in db_settings
        assert "user" in db_settings
        assert "password" in db_settings
        assert "host" in db_settings
        assert "port" in db_settings
    
    def test_path_prefix_starts_with_slash(self):
        """Test that PATH_PREFIX starts with slash."""
        assert settings.PATH_PREFIX.startswith("/")
    
    def test_app_port_is_integer(self):
        """Test that APP_PORT is integer."""
        assert isinstance(settings.APP_PORT, int)
    
    def test_db_context_returns_dict(self):
        """Test that db_context returns a dictionary."""
        context = settings.db_context
        assert isinstance(context, dict)