# test_session_manager.py
import pytest
from app.db.connection.session import SessionManager


def test_session_manager_singleton():
    """Test that SessionManager follows singleton pattern."""
    a = SessionManager()
    b = SessionManager()
    
    assert a is b
    assert id(a) == id(b)


@pytest.mark.asyncio
async def test_session_manager_engine():
    """Test that SessionManager creates engine properly."""
    sm = SessionManager()
    assert sm.engine is not None
    
    # Проверяем, что движок создан корректно
    from sqlalchemy.ext.asyncio import AsyncEngine
    assert isinstance(sm.engine, AsyncEngine)
    
    # Cleanup
    await sm.engine.dispose()