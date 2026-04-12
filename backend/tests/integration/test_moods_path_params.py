import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/moods/not-a-uuid", "/moods/123"])
async def test_get_mood_invalid_uuid_returns_422(app, path: str):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(path)
        assert resp.status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/moods/not-a-uuid", "/moods/123"])
async def test_delete_mood_invalid_uuid_returns_422(app, path: str):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.delete(path)
        assert resp.status_code == 422
