"""
Unit tests for recurring tasks functionality.
"""
import pytest
from datetime import date, timedelta
from src.todo_app.models.task import Task


def test_task_is_recurring():
    """Test the is_recurring method."""
    # Non-recurring task
    task1 = Task(id=1, title="Non-recurring task", recurrence="none")
    assert task1.is_recurring() is False

    # Recurring tasks
    task2 = Task(id=2, title="Daily task", recurrence="daily")
    assert task2.is_recurring() is True

    task3 = Task(id=3, title="Weekly task", recurrence="weekly")
    assert task3.is_recurring() is True

    task4 = Task(id=4, title="Monthly task", recurrence="monthly")
    assert task4.is_recurring() is True


def test_get_next_occurrence_date():
    """Test the get_next_occurrence_date method."""
    test_date = date(2023, 1, 15)  # Jan 15, 2023

    # Non-recurring task
    task_none = Task(id=1, title="Non-recurring", recurrence="none")
    assert task_none.get_next_occurrence_date(test_date) is None

    # Daily recurring task
    task_daily = Task(id=2, title="Daily", recurrence="daily")
    next_date = task_daily.get_next_occurrence_date(test_date)
    expected = test_date + timedelta(days=1)
    assert next_date == expected

    # Weekly recurring task
    task_weekly = Task(id=3, title="Weekly", recurrence="weekly")
    next_date = task_weekly.get_next_occurrence_date(test_date)
    expected = test_date + timedelta(weeks=1)
    assert next_date == expected

    # Monthly recurring task
    task_monthly = Task(id=4, title="Monthly", recurrence="monthly")
    next_date = task_monthly.get_next_occurrence_date(test_date)
    expected = date(2023, 2, 15)  # Feb 15, 2023
    assert next_date == expected

    # Monthly recurring task - edge case for Jan 31
    jan_31 = date(2023, 1, 31)
    task_monthly_edge = Task(id=5, title="Monthly edge", recurrence="monthly")
    next_date = task_monthly_edge.get_next_occurrence_date(jan_31)
    # Jan 31 -> Feb 28 (since Feb doesn't have 31 days)
    expected = date(2023, 2, 28)
    assert next_date == expected

    # Monthly recurring task - leap year
    feb_29_2024 = date(2024, 2, 29)  # Leap year
    task_leap = Task(id=6, title="Leap year", recurrence="monthly")
    next_date = task_leap.get_next_occurrence_date(feb_29_2024)
    expected = date(2024, 3, 29)
    assert next_date == expected