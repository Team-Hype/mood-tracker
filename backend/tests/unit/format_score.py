# tests/unit/format_score.py
import pytest
from frontend.common import format_score


class TestFormatScore:
    """Tests for format_score function."""
    
    def test_format_score_with_float(self):
        """Test formatting float score."""
        assert format_score(4.0) == "4.00/5"
        assert format_score(3.5) == "3.50/5"
        assert format_score(2.75) == "2.75/5"
    
    def test_format_score_with_int(self):
        """Test formatting integer score."""
        assert format_score(4) == "4.00/5"
        assert format_score(5) == "5.00/5"
        assert format_score(1) == "1.00/5"
    
    def test_format_score_with_zero(self):
        """Test formatting zero score."""
        assert format_score(0) == "0.00/5"
    
    def test_format_score_rounding(self):
        """Test proper rounding of scores."""
        assert format_score(3.333) == "3.33/5"
        assert format_score(3.335) == "3.34/5"