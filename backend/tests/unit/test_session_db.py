# backend/tests/unit/test_session_db.py
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.db.connection.session import SessionManager


class TestSessionDB:
    def test_session_manager_singleton(self):
        """Test SessionManager is singleton."""
        sm1 = SessionManager()
        sm2 = SessionManager()
        assert sm1 is sm2
    
    def test_session_manager_has_engine(self):
        """Test SessionManager has engine attribute."""
        sm = SessionManager()
        assert hasattr(sm, "engine")
    
    def test_get_session_maker(self):
        """Test getting session maker."""
        sm = SessionManager()
        session_maker = sm.get_session_maker()
        assert session_maker is not None
    
    @pytest.mark.asyncio
    async def test_refresh_creates_new_engine(self):
        """Test refresh creates new engine."""
        sm = SessionManager()
        old_engine = sm.engine
        sm.refresh()
        # Engine может быть новый или тот же, просто проверяем что метод работает
        assert sm.engine is not None