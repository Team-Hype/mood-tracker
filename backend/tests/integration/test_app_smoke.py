import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_swagger_is_available(app):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/swagger")

    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
