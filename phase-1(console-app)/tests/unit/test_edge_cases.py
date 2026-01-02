"""
Unit tests for edge case handling.
"""
import pytest
from src.todo_app.utils.validators import validate_date_edge_cases


def test_validate_invalid_date_formats():
    """Test validation of invalid date formats."""
    # Test invalid day
    errors = validate_date_edge_cases("32-Jan")
    assert len(errors) > 0
    assert any("32" in error and "Day must be between 1 and 31" in error for error in errors)

    # Test invalid month
    errors = validate_date_edge_cases("15-Foo")
    assert len(errors) > 0
    assert any("Foo" in error and "Must be a valid 3-letter month abbreviation" in error for error in errors)

    # Test invalid format
    errors = validate_date_edge_cases("15January")
    assert len(errors) > 0
    assert any("Expected format: DD-MMM" in error for error in errors)

    # Test impossible February dates
    errors = validate_date_edge_cases("30-Feb")
    assert len(errors) > 0
    assert any("February cannot have more than 29 days" in error for error in errors)

    # Test impossible dates for 30-day months
    errors = validate_date_edge_cases("31-Apr")
    assert len(errors) > 0
    assert any("Apr cannot have more than 30 days" in error for error in errors)

    errors = validate_date_edge_cases("31-Jun")
    assert len(errors) > 0
    assert any("Jun cannot have more than 30 days" in error for error in errors)

    errors = validate_date_edge_cases("31-Sep")
    assert len(errors) > 0
    assert any("Sep cannot have more than 30 days" in error for error in errors)

    errors = validate_date_edge_cases("31-Nov")
    assert len(errors) > 0
    assert any("Nov cannot have more than 30 days" in error for error in errors)

    # Test valid dates should have no errors
    errors = validate_date_edge_cases("29-Feb")  # This is allowed, though the actual validation happens elsewhere
    assert len(errors) == 0

    errors = validate_date_edge_cases("28-Feb")
    assert len(errors) == 0

    errors = validate_date_edge_cases("30-Apr")
    assert len(errors) == 0

    errors = validate_date_edge_cases("31-Jan")
    assert len(errors) == 0


def test_validate_edge_case_empty_and_none():
    """Test validation of empty and None date values."""
    errors = validate_date_edge_cases("")
    assert len(errors) == 0  # Empty should be valid (optional field)

    errors = validate_date_edge_cases(None)
    assert len(errors) == 0  # None should be valid (optional field)