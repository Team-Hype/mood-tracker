from datetime import datetime
from frontend.common import to_domain_entries


def test_to_domain_entries():
    raw = [
        {
            "id": "1",
            "username": "A",
            "mood_entry": 3,
            "mood_emoji": "😐",
            "comment": "ok",
            "created_at": "2024-01-01T00:00:00",
        }
    ]

    result = to_domain_entries(raw)

    assert len(result) == 1
    assert result[0].username == "A"
    assert result[0].mood_entry == "3"  # Строка, не int
    assert result[0].mood_emoji == "😐"
    assert result[0].comment == "ok"
    assert isinstance(result[0].created_at, datetime)


def test_to_domain_entries_with_datetime_object():
    """Test with datetime object instead of string."""
    now = datetime.now()
    raw = [
        {
            "id": "2",
            "username": "B",
            "mood_entry": 5,
            "mood_emoji": "😄",
            "comment": "Awesome!",
            "created_at": now,
        }
    ]

    result = to_domain_entries(raw)
    assert result[0].created_at == now
    assert result[0].mood_entry == "5"  # Строка, не int
