from httpx import AsyncClient, ASGITransport
from app.src.app import app


async def test_lifespan_with_db_operations():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        _response = await client.get("/mood/")
