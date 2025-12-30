"""
Unit tests for CLI commands.
"""
import pytest
import sys
from io import StringIO
from unittest.mock import Mock, patch
from src.todo_app.cli.commands import add_task, list_tasks, update_task, delete_task
from src.todo_app.models.task_manager import TaskManager


def test_add_task():
    """Test the add_task command function."""
    # Create a mock args object
    class MockArgs:
        title = "Test task"
        description = "Test description"
        priority = "high"
        tags = ["work", "urgent"]
        due_date = None
        recurring = "none"

    args = MockArgs()

    # Create a mock task manager
    with patch('src.todo_app.models.task_manager.TaskManager') as mock_tm_class:
        mock_task_manager = Mock()
        mock_task = Mock()
        mock_task.id = 1
        mock_task_manager.add_task.return_value = mock_task
        mock_tm_class.return_value = mock_task_manager

        # Capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        add_task(args, mock_task_manager)

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check that add_task was called with the right parameters
        mock_task_manager.add_task.assert_called_once_with(
            title="Test task",
            description="Test description",
            priority="high",
            tags=["work", "urgent"],
            due_date=None,
            recurrence="none"
        )

        # Check that the success message was printed
        output = captured_output.getvalue().strip()
        assert "Task added successfully with ID: 1" in output


def test_list_tasks():
    """Test the list_tasks command function."""
    # Create a mock args object
    class MockArgs:
        status = None
        priority = None
        sort = None

    args = MockArgs()

    # Create a mock task manager
    with patch('src.todo_app.models.task_manager.TaskManager') as mock_tm_class:
        mock_task_manager = Mock()
        mock_task = Mock()
        mock_task.id = 1
        mock_task.status = "pending"
        mock_task.priority = "high"
        mock_task.title = "Test task"
        mock_task.due_date = None
        mock_task.tags = ["work"]
        mock_task_manager.list_tasks.return_value = [mock_task]
        mock_tm_class.return_value = mock_task_manager

        # Capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        list_tasks(args, mock_task_manager)

        # Restore stdout
        sys.stdout = sys.__stdout__

        # Check that list_tasks was called with the right parameters
        mock_task_manager.list_tasks.assert_called_once_with(
            status=None,
            priority=None,
            sort_by=None
        )

        # Check that the output contains the task
        output = captured_output.getvalue()
        assert "ID" in output
        assert "Status" in output
        assert "Test task" in output


def test_update_task():
    """Test the update_task command function."""
    # Create a mock args object
    class MockArgs:
        id = 1
        title = "Updated task"
        description = "Updated description"
        status = "complete"
        priority = "low"
        tags = ["updated", "test"]
        due_date = None

    args = MockArgs()

    # Create a mock task manager
    mock_task_manager = Mock()
    mock_task = Mock()
    mock_task.id = 1
    mock_task_manager.update_task.return_value = mock_task

    # Capture print output
    captured_output = StringIO()
    sys.stdout = captured_output

    update_task(args, mock_task_manager)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that update_task was called with the right parameters (due_date is not passed when None)
    mock_task_manager.update_task.assert_called_once_with(
        1,
        title="Updated task",
        description="Updated description",
        status="complete",
        priority="low",
        tags=["updated", "test"]
    )

    # Check that the success message was printed
    output = captured_output.getvalue().strip()
    assert "Task 1 updated successfully" in output


def test_delete_task():
    """Test the delete_task command function."""
    # Create a mock args object
    class MockArgs:
        id = 1

    args = MockArgs()

    # Create a mock task manager
    mock_task_manager = Mock()
    mock_task_manager.delete_task.return_value = True

    # Capture print output
    captured_output = StringIO()
    sys.stdout = captured_output

    delete_task(args, mock_task_manager)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that delete_task was called with the right parameters
    mock_task_manager.delete_task.assert_called_once_with(1)

    # Check that the success message was printed
    output = captured_output.getvalue().strip()
    assert "Task 1 deleted successfully" in output


def test_toggle_task():
    """Test the toggle_task command function."""
    # Create a mock args object
    class MockArgs:
        id = 1

    args = MockArgs()

    # Create a mock task manager
    mock_task_manager = Mock()
    mock_task = Mock()
    mock_task.id = 1
    mock_task.status = "complete"
    mock_task_manager.toggle_task_status.return_value = mock_task

    # Capture print output
    captured_output = StringIO()
    sys.stdout = captured_output

    from src.todo_app.cli.commands import toggle_task
    toggle_task(args, mock_task_manager)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that toggle_task_status was called with the right parameters
    mock_task_manager.toggle_task_status.assert_called_once_with(1)

    # Check that the success message was printed
    output = captured_output.getvalue().strip()
    assert "status toggled to" in output


def test_search_tasks():
    """Test the search_tasks command function."""
    # Create a mock args object
    class MockArgs:
        query = "test"

    args = MockArgs()

    # Create a mock task manager
    mock_task_manager = Mock()
    mock_task = Mock()
    mock_task.id = 1
    mock_task.status = "pending"
    mock_task.priority = "high"
    mock_task.title = "Test task"
    mock_task.due_date = None
    mock_task.tags = ["work"]
    mock_task_manager.search_tasks.return_value = [mock_task]

    # Capture print output
    captured_output = StringIO()
    sys.stdout = captured_output

    from src.todo_app.cli.commands import search_tasks
    search_tasks(args, mock_task_manager)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check that search_tasks was called with the right parameters
    mock_task_manager.search_tasks.assert_called_once_with("test")

    # Check that the output contains the task
    output = captured_output.getvalue()
    assert "ID" in output
    assert "Status" in output
    assert "Test task" in output