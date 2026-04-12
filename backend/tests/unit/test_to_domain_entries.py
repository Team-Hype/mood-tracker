# test_to_domain_entries.py
from datetime import datetime
from frontend.common import to_domain_entries


def test_to_domain_entries():
    raw = [
        {
            "id": "1",  # API возвращает строку
            "user": "A",
            "mood": 3,
            "comment": "ok",
            "date": "2024-01-01T00:00:00",
        }
    ]

    result = to_domain_entries(raw)

    assert len(result) == 1
    assert result[0].user == "A"
    assert result[0].mood == 3
    assert result[0].comment == "ok"
    assert isinstance(result[0].date, datetime)


def test_to_domain_entries_with_datetime_object():
    """Test with datetime object instead of string."""
    now = datetime.now()
    raw = [
        {
            "id": "2",
            "user": "B",
            "mood": 5,
            "comment": "Awesome!",
            "date": now,
        }
    ]

    result = to_domain_entries(raw)
    assert result[0].date == now