"""
Unit tests for validation utilities.
"""
import pytest
from datetime import date
from src.todo_app.utils.validators import (
    validate_title, validate_description, validate_status,
    validate_priority, validate_tag, validate_tags, validate_recurrence,
    validate_date_format, parse_date_string, validate_task_data
)


def test_validate_title():
    """Test title validation."""
    # Valid titles
    assert validate_title("Valid title") is True
    assert validate_title("x" * 200) is True  # Maximum length

    # Invalid titles
    assert validate_title("") is False
    assert validate_title("   ") is False  # Only whitespace
    assert validate_title("x" * 201) is False  # Too long


def test_validate_description():
    """Test description validation."""
    # Valid descriptions
    assert validate_description("") is True
    assert validate_description("Valid description") is True
    assert validate_description("x" * 1000) is True  # Maximum length

    # Invalid descriptions
    assert validate_description("x" * 1001) is False  # Too long


def test_validate_status():
    """Test status validation."""
    # Valid statuses
    assert validate_status("pending") is True
    assert validate_status("complete") is True

    # Invalid status
    assert validate_status("invalid") is False
    assert validate_status("") is False


def test_validate_priority():
    """Test priority validation."""
    # Valid priorities
    assert validate_priority("high") is True
    assert validate_priority("medium") is True
    assert validate_priority("low") is True

    # Invalid priority
    assert validate_priority("invalid") is False
    assert validate_priority("") is False


def test_validate_tag():
    """Test tag validation."""
    # Valid tags
    assert validate_tag("valid-tag") is True
    assert validate_tag("valid_tag") is True
    assert validate_tag("valid123") is True
    assert validate_tag("a" * 50) is True  # Maximum length

    # Invalid tags
    assert validate_tag("invalid@tag") is False  # Special character
    assert validate_tag("a" * 51) is False  # Too long
    assert validate_tag("") is False


def test_validate_tags():
    """Test tags list validation."""
    # Valid tag lists
    assert validate_tags([]) is True
    assert validate_tags(["tag1", "tag2"]) is True
    assert validate_tags(["valid-tag"] * 10) is True  # Maximum count

    # Invalid tag lists
    assert validate_tags(["valid-tag"] * 11) is False  # Too many tags
    assert validate_tags(["valid-tag", "invalid@tag"]) is False  # Invalid tag


def test_validate_recurrence():
    """Test recurrence validation."""
    # Valid recurrence values
    assert validate_recurrence("daily") is True
    assert validate_recurrence("weekly") is True
    assert validate_recurrence("monthly") is True
    assert validate_recurrence("none") is True

    # Invalid recurrence
    assert validate_recurrence("invalid") is False


def test_validate_date_format():
    """Test date format validation."""
    # Valid date formats
    assert validate_date_format("05-Jan") is True
    assert validate_date_format("31-Dec") is True
    assert validate_date_format("01-Jan") is True
    assert validate_date_format("5-Jan") is True  # Single digit day is valid (format is still D-MMM)
    assert validate_date_format("") is True  # Optional date
    assert validate_date_format(None) is True  # Optional date

    # Invalid date formats
    assert validate_date_format("32-Jan") is False  # Invalid day
    assert validate_date_format("05-Invalid") is False  # Invalid month
    assert validate_date_format("05") is False  # Missing month
    assert validate_date_format("05-") is False  # Missing month part
    assert validate_date_format("05-January") is False  # Full month name


def test_parse_date_string():
    """Test date string parsing."""
    # Valid date parsing
    result = parse_date_string("05-Jan")
    assert result is not None
    assert result.day == 5
    assert result.month == 1

    # Test with past date (should use next year)
    result = parse_date_string("01-Jan")  # Assuming Jan 1 is in the past
    assert result is not None

    # Test invalid date
    result = parse_date_string("32-Jan")
    assert result is None

    # Test None/empty input
    assert parse_date_string(None) is None
    assert parse_date_string("") is None


def test_validate_task_data():
    """Test comprehensive task data validation."""
    # Valid task data
    errors = validate_task_data(
        title="Valid title",
        description="Valid description",
        status="pending",
        priority="high",
        tags=["tag1", "tag2"],
        due_date="05-Jan",
        recurrence="weekly"
    )
    assert len(errors) == 0

    # Invalid task data
    errors = validate_task_data(
        title="",  # Invalid
        description="x" * 1001,  # Invalid
        status="invalid",  # Invalid
        priority="invalid",  # Invalid
        tags=["invalid@tag"],  # Invalid
        due_date="32-Jan",  # Invalid date format
        recurrence="invalid"  # Invalid
    )
    assert len(errors) == 7  # All fields invalid (including the date format error)