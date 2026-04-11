import pytest
from httpx import ASGITransport, AsyncClient

from app.src.settings import settings


@pytest.mark.asyncio
async def test_swagger_is_available(app):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(settings.SWAGGER_PATH)

    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
