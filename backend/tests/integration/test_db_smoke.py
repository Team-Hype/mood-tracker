import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_db_connection_smoke():
    from app.db.connection.session import SessionManager

    session_maker = SessionManager().get_session_maker()

    async with session_maker() as session:
        value = await session.scalar(text("SELECT 1"))
        assert value == 1
