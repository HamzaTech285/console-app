"""
Unit tests for the Task class.
"""
import pytest
from datetime import date
from src.todo_app.models.task import Task


def test_task_creation():
    """Test creating a basic task with required fields."""
    task = Task(id=1, title="Test task")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == ""
    assert task.status == "pending"
    assert task.priority == "medium"
    assert task.tags == []
    assert task.due_date is None
    assert task.recurrence == "none"
    assert task.created_at == date.today()


def test_task_creation_with_all_fields():
    """Test creating a task with all fields specified."""
    test_date = date(2023, 12, 25)
    task = Task(
        id=1,
        title="Test task",
        description="Test description",
        status="complete",
        priority="high",
        tags=["work", "urgent"],
        due_date=test_date,
        recurrence="weekly"
    )

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.status == "complete"
    assert task.priority == "high"
    assert task.tags == ["work", "urgent"]
    assert task.due_date == test_date
    assert task.recurrence == "weekly"


def test_task_title_validation():
    """Test validation of task title."""
    # Test empty title
    with pytest.raises(ValueError, match="Title is required and cannot be empty"):
        Task(id=1, title="")

    # Test whitespace-only title
    with pytest.raises(ValueError, match="Title is required and cannot be empty"):
        Task(id=1, title="   ")

    # Test title that's too long
    long_title = "x" * 201
    with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
        Task(id=1, title=long_title)


def test_task_description_validation():
    """Test validation of task description."""
    # Test description that's too long
    long_description = "x" * 1001
    with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
        Task(id=1, title="Test", description=long_description)


def test_task_status_validation():
    """Test validation of task status."""
    # Test invalid status
    with pytest.raises(ValueError, match="Status must be 'pending' or 'complete'"):
        Task(id=1, title="Test", status="invalid")


def test_task_priority_validation():
    """Test validation of task priority."""
    # Test invalid priority
    with pytest.raises(ValueError, match="Priority must be 'high', 'medium', or 'low'"):
        Task(id=1, title="Test", priority="invalid")


def test_task_tag_validation():
    """Test validation of task tags."""
    # Test too many tags
    with pytest.raises(ValueError, match="A task cannot have more than 10 tags"):
        Task(id=1, title="Test", tags=["tag" + str(i) for i in range(11)])

    # Test invalid tag characters
    with pytest.raises(ValueError, match="contains invalid character"):
        Task(id=1, title="Test", tags=["valid-tag", "invalid@tag"])


def test_task_recurrence_validation():
    """Test validation of task recurrence."""
    # Test invalid recurrence
    with pytest.raises(ValueError, match="Recurrence must be 'daily', 'weekly', 'monthly', or 'none'"):
        Task(id=1, title="Test", recurrence="invalid")


def test_toggle_status():
    """Test toggling task status."""
    task = Task(id=1, title="Test task", status="pending")

    # Toggle from pending to complete
    task.toggle_status()
    assert task.status == "complete"

    # Toggle from complete to pending
    task.toggle_status()
    assert task.status == "pending"