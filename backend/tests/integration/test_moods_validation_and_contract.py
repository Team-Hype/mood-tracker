import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_post_mood_without_comment_returns_null_comment(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/moods", json={"username": "anna", "mood_entry": "Good"})
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["comment"] is None


@pytest.mark.asyncio
async def test_post_mood_emoji_matches_entry(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        cases = {
            "Rough": "😡",
            "Low": "😔",
            "Okay": "😐",
            "Good": "🙂",
            "Great": "😄",
        }

        for mood_entry, expected_emoji in cases.items():
            resp = await client.post("/moods", json={"username": "u", "mood_entry": mood_entry})
            assert resp.status_code == 201, resp.text
            data = resp.json()
            assert data["mood_entry"] == mood_entry
            assert data["mood_emoji"] == expected_emoji


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"mood_entry": "Good"},
        {"username": "x"},
        {"username": "", "mood_entry": "Good"},
    ],
)
async def test_post_mood_pydantic_validation_422(app, payload):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/moods", json=payload)
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_post_mood_username_too_long_422(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/moods",
            json={"username": "a" * 51, "mood_entry": "Good"},
        )
        assert resp.status_code == 422


@pytest.mark.asyncio
async def test_post_mood_comment_too_long_422(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/moods",
            json={"username": "u", "mood_entry": "Good", "comment": "x" * 501},
        )
        assert resp.status_code == 422
