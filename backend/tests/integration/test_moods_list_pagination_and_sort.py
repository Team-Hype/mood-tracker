import asyncio
from datetime import datetime
from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient


async def _create(client: AsyncClient, username: str, mood_entry: str, comment: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"username": username, "mood_entry": mood_entry}
    if comment is not None:
        payload["comment"] = comment
    resp = await client.post("/moods", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


@pytest.mark.asyncio
async def test_get_moods_sorted_by_created_at_desc(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        a = await _create(client, "u1", "Good")
        await asyncio.sleep(0.01)
        b = await _create(client, "u1", "Great")
        await asyncio.sleep(0.01)
        c = await _create(client, "u1", "Low")

        resp = await client.get("/moods")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3

        created = [datetime.fromisoformat(item["created_at"]) for item in data]
        assert created == sorted(created, reverse=True)

        assert data[0]["id"] == c["id"]
        assert data[1]["id"] == b["id"]
        assert data[2]["id"] == a["id"]


@pytest.mark.asyncio
async def test_get_moods_limit_and_offset(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        created_ids = []
        for i in range(5):
            item = await _create(client, "pager", "Okay", comment=f"#{i}")
            created_ids.append(item["id"])

        resp_all = await client.get("/moods")
        assert resp_all.status_code == 200
        all_items = resp_all.json()
        assert [x["id"] for x in all_items] == list(reversed(created_ids))

        resp_limit = await client.get("/moods?limit=2")
        assert resp_limit.status_code == 200
        limit_items = resp_limit.json()
        assert len(limit_items) == 2
        assert [x["id"] for x in limit_items] == list(reversed(created_ids))[:2]

        resp_page = await client.get("/moods?limit=2&offset=2")
        assert resp_page.status_code == 200
        page_items = resp_page.json()
        assert len(page_items) == 2
        assert [x["id"] for x in page_items] == list(reversed(created_ids))[2:4]

        resp_empty = await client.get("/moods?offset=999")
        assert resp_empty.status_code == 200
        assert resp_empty.json() == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query",
    [
        "limit=0",
        "limit=1001",
        "offset=-1",
    ],
)
async def test_get_moods_invalid_pagination_params_422(app, query: str):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(f"/moods?{query}")
        assert resp.status_code == 422
