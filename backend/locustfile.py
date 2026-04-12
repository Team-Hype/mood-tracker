import os
import random
import string
from datetime import datetime
from typing import Any

from locust import HttpUser, task, between

MOODS = ["Rough", "Low", "Okay", "Good", "Great"]

def _rand_suffix(n: int = 8) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


class MoodTrackerUser(HttpUser):
    """
    Load profile:
    - create mood entry (POST /moods)
    - list moods (GET /moods?username=...)
    - get mood by id (GET /moods/{id}) sometimes
    """

    # wait time between tasks per user
    wait_time = between(0.2, 1.0)

    def on_start(self) -> None:
        # unique user per locust user instance, so filtering makes sense
        self.username = f"load_{_rand_suffix()}"
        self.created_ids: list[str] = []

    @task(5)
    def create_mood(self) -> None:
        payload: dict[str, Any] = {
            "username": self.username,
            "mood_entry": random.choice(MOODS),
            "comment": f"load-test {datetime.utcnow().isoformat()}",
        }
        with self.client.post("/moods", json=payload, name="POST /moods", catch_response=True) as resp:
            if resp.status_code != 201:
                resp.failure(f"Expected 201, got {resp.status_code}: {resp.text}")
                return

            try:
                data = resp.json()
                mood_id = data["id"]
                self.created_ids.append(mood_id)
            except Exception as e:
                resp.failure(f"Invalid JSON response: {e}")

    @task(3)
    def list_moods_for_user(self) -> None:
        # limit small so list is not too heavy
        params = {"username": self.username, "limit": 20, "offset": 0}
        with self.client.get("/moods", params=params, name="GET /moods?username", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Expected 200, got {resp.status_code}: {resp.text}")

    @task(1)
    def get_mood_by_id(self) -> None:
        if not self.created_ids:
            return
        mood_id = random.choice(self.created_ids)
        with self.client.get(f"/moods/{mood_id}", name="GET /moods/{id}", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Expected 200, got {resp.status_code}: {resp.text}")
