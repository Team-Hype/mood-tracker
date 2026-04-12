# backend/tests/unit/test_session_manager_advanced.py
import pytest
from app.db.connection.session import SessionManager


class TestSessionManagerAdvanced:
    """Advanced tests for SessionManager."""
    
    def test_session_manager_singleton(self):
        """Test that SessionManager follows singleton pattern."""
        sm1 = SessionManager()
        sm2 = SessionManager()
        assert sm1 is sm2
    
    def test_session_manager_has_engine(self):
        """Test that SessionManager has engine attribute."""
        sm = SessionManager()
        assert hasattr(sm, "engine")
        assert sm.engine is not None
    
    def test_session_manager_get_session_maker(self):
        """Test getting session maker."""
        sm = SessionManager()
        session_maker = sm.get_session_maker()
        assert session_maker is not None
        assert hasattr(session_maker, "__call__")