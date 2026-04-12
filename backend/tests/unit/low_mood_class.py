# backend/tests/unit/test_lifespan_coverage.py
import pytest
from unittest.mock import AsyncMock, patch


class TestLifespanCoverage:
    """Tests to improve lifespan.py coverage."""
    
    @pytest.mark.asyncio
    async def test_lifespan_successful_connection(self):
        """Test lifespan with successful DB connection."""
        from app.src.lifespan import lifespan
        from fastapi import FastAPI
        
        app = FastAPI()
        
        with patch('app.src.lifespan.SessionManager') as MockSM:
            mock_sm = MockSM.return_value
            mock_session = AsyncMock()
            mock_session.execute = AsyncMock()
            mock_session_maker = AsyncMock()
            mock_session_maker.__aenter__.return_value = mock_session
            mock_sm.get_session_maker.return_value = mock_session_maker
            mock_sm.engine.dispose = AsyncMock()
            
            async with lifespan(app):
                pass
            
            mock_sm.engine.dispose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_lifespan_db_error(self):
        """Test lifespan with DB connection error."""
        from app.src.lifespan import lifespan
        from fastapi import FastAPI
        
        app = FastAPI()
        
        with patch('app.src.lifespan.SessionManager') as MockSM:
            mock_sm = MockSM.return_value
            mock_sm.get_session_maker.side_effect = Exception("DB connection failed")
            mock_sm.engine.dispose = AsyncMock()
            
            async with lifespan(app):
                pass
            
            mock_sm.engine.dispose.assert_called_once()