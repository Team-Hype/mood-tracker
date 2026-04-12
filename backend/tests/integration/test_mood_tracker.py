import uuid
import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_get_moods_empty_list(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/moods")
        assert response.status_code == 200
        assert response.json() == []


@pytest.mark.asyncio
async def test_create_mood_success(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"username": "anna", "mood_entry": "Great", "comment": "Awesome day!"}
        response = await client.post("/moods", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "anna"
        assert data["mood_entry"] == "Great"
        assert data["mood_emoji"] == "😄"
        assert data["comment"] == "Awesome day!"
        assert "id" in data
        assert "created_at" in data


@pytest.mark.asyncio
async def test_create_mood_invalid_mood_entry(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"username": "bob", "mood_entry": "Terrible", "comment": "Bad day"}
        response = await client.post("/moods", json=payload)
        assert response.status_code == 422
        assert "mood_entry must be one of" in response.text


@pytest.mark.asyncio
async def test_get_mood_by_id_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post(
            "/moods",
            json={"username": "charlie", "mood_entry": "Good", "comment": "Nice"},
        )
        mood_id = create_resp.json()["id"]

        get_resp = await client.get(f"/moods/{mood_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == mood_id


@pytest.mark.asyncio
async def test_get_mood_by_id_not_found(app):
    fake_id = uuid.uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/moods/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Mood entry not found"


@pytest.mark.asyncio
async def test_delete_mood_success(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        create_resp = await client.post(
            "/moods", json={"username": "dave", "mood_entry": "Okay", "comment": "Meh"}
        )
        mood_id = create_resp.json()["id"]

        delete_resp = await client.delete(f"/moods/{mood_id}")
        assert delete_resp.status_code == 204

        get_resp = await client.get(f"/moods/{mood_id}")
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_mood_not_found(app):
    fake_id = uuid.uuid4()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.delete(f"/moods/{fake_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Mood entry not found"


@pytest.mark.asyncio
async def test_get_moods_with_username_filter(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/moods", json={"username": "emily", "mood_entry": "Great"})
        await client.post("/moods", json={"username": "frank", "mood_entry": "Low"})

        resp = await client.get("/moods?username=emily")
        assert resp.status_code == 200
        entries = resp.json()
        assert len(entries) == 1
        assert entries[0]["username"] == "emily"
