# backend/tests/unit/test_lifespan.py
import pytest
from unittest.mock import AsyncMock, patch


class TestLifespan:
    """Tests for application lifespan."""
    
    @pytest.mark.asyncio
    async def test_lifespan_success(self):
        """Test lifespan with successful DB connection."""
        from app.src.lifespan import lifespan
        from fastapi import FastAPI
        
        app = FastAPI()
        
        with patch('app.src.lifespan.SessionManager') as MockSM:
            mock_sm = MockSM.return_value
            mock_session = AsyncMock()
            mock_session.execute = AsyncMock()
            mock_sm.get_session_maker.return_value.__aenter__.return_value = mock_session
            
            async with lifespan(app):
                pass
            
            # Проверяем, что dispose был вызван
            mock_sm.engine.dispose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_db_error(self):
        """Test lifespan with DB connection error."""
        from app.src.lifespan import lifespan
        from fastapi import FastAPI
        
        app = FastAPI()
        
        with patch('app.src.lifespan.SessionManager') as MockSM:
            mock_sm = MockSM.return_value
            mock_sm.get_session_maker.side_effect = Exception("DB Error")
            
            async with lifespan(app):
                pass  # Должно перехватить ошибку и продолжить