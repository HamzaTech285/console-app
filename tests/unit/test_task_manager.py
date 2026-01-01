"""
Unit tests for the TaskManager class.
"""
import os
import tempfile
from datetime import date
from src.todo_app.models.task_manager import TaskManager
from src.todo_app.models.task import Task


def test_task_manager_initialization():
    """Test initializing a TaskManager."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Clean up if file exists
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

        task_manager = TaskManager(storage_path=tmp_path)

        assert len(task_manager.tasks) == 0
        assert task_manager.next_id == 1
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_add_task():
    """Test adding a task to the TaskManager."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        task = task_manager.add_task(title="Test task", description="Test description")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert len(task_manager.tasks) == 1
        assert task_manager.tasks[1] == task
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_get_task():
    """Test retrieving a task by ID."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add a task
        task = task_manager.add_task(title="Test task")

        # Retrieve the task
        retrieved_task = task_manager.get_task(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title

        # Try to retrieve a non-existent task
        non_existent_task = task_manager.get_task(999)
        assert non_existent_task is None
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_update_task():
    """Test updating a task."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add a task
        original_task = task_manager.add_task(title="Original task", priority="low")

        # Update the task
        updated_task = task_manager.update_task(
            task_id=original_task.id,
            title="Updated task",
            priority="high"
        )

        assert updated_task is not None
        assert updated_task.title == "Updated task"
        assert updated_task.priority == "high"

        # Verify the task in the manager was also updated
        retrieved_task = task_manager.get_task(original_task.id)
        assert retrieved_task.title == "Updated task"
        assert retrieved_task.priority == "high"
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_delete_task():
    """Test deleting a task."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add a task
        task = task_manager.add_task(title="Test task")

        # Verify task exists
        assert task_manager.get_task(task.id) is not None

        # Delete the task
        result = task_manager.delete_task(task.id)

        assert result is True
        assert task_manager.get_task(task.id) is None
        assert len(task_manager.tasks) == 0

        # Try to delete a non-existent task
        result = task_manager.delete_task(999)
        assert result is False
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_list_tasks():
    """Test listing tasks with filters."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add multiple tasks with different attributes
        task1 = task_manager.add_task(title="Task 1", priority="high")
        task2 = task_manager.add_task(title="Task 2", priority="low")
        task3 = task_manager.add_task(title="Task 3", priority="medium")

        # Update task2 status to complete
        task_manager.update_task(task2.id, status="complete")

        # List all tasks
        all_tasks = task_manager.list_tasks()
        assert len(all_tasks) == 3

        # List tasks with pending status
        pending_tasks = task_manager.list_tasks(status="pending")
        assert len(pending_tasks) == 2
        assert all(task.status == "pending" for task in pending_tasks)

        # List tasks with high priority
        high_priority_tasks = task_manager.list_tasks(priority="high")
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].priority == "high"

        # List tasks with pending status and medium priority
        filtered_tasks = task_manager.list_tasks(status="pending", priority="medium")
        assert len(filtered_tasks) == 1
        assert filtered_tasks[0].status == "pending"
        assert filtered_tasks[0].priority == "medium"
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_search_tasks():
    """Test searching tasks."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add tasks with different content
        task1 = task_manager.add_task(title="Buy groceries", description="Milk and bread", tags=["shopping"])
        task2 = task_manager.add_task(title="Finish report", description="Complete the quarterly report", tags=["work"])
        task3 = task_manager.add_task(title="Call mom", description="Check in with mom", tags=["family"])

        # Search by title
        results = task_manager.search_tasks("groceries")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"

        # Search by description
        results = task_manager.search_tasks("report")
        assert len(results) == 1
        assert results[0].title == "Finish report"

        # Search by tag
        results = task_manager.search_tasks("shopping")
        assert len(results) == 1
        assert results[0].title == "Buy groceries"

        # Search with no matches
        results = task_manager.search_tasks("nonexistent")
        assert len(results) == 0
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_toggle_task_status():
    """Test toggling task status."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add a task (defaults to pending status)
        task = task_manager.add_task(title="Test task")

        # Toggle the status
        toggled_task = task_manager.toggle_task_status(task.id)

        assert toggled_task is not None
        assert toggled_task.status == "complete"

        # Toggle back to pending
        toggled_task = task_manager.toggle_task_status(task.id)
        assert toggled_task.status == "pending"

        # Try to toggle non-existent task
        result = task_manager.toggle_task_status(999)
        assert result is None
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_persistence():
    """Test that tasks are saved to and loaded from storage."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Create a task manager and add tasks
        task_manager1 = TaskManager(storage_path=tmp_path)
        task1 = task_manager1.add_task(title="Task 1", description="Description 1", priority="high")
        task2 = task_manager1.add_task(title="Task 2", description="Description 2", priority="low")

        # Create a new task manager with the same storage path
        task_manager2 = TaskManager(storage_path=tmp_path)

        # Verify that the tasks were loaded
        assert len(task_manager2.tasks) == 2
        assert task_manager2.get_task(task1.id) is not None
        assert task_manager2.get_task(task2.id) is not None
        assert task_manager2.get_task(task1.id).title == "Task 1"
        assert task_manager2.get_task(task2.id).title == "Task 2"
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_sort_tasks():
    """Test sorting tasks by different criteria."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add tasks with different priorities and due dates
        task1 = task_manager.add_task(title="Task 1", priority="low")
        task2 = task_manager.add_task(title="Task 2", priority="high")
        task3 = task_manager.add_task(title="Task 3", priority="medium")

        # Test sorting by priority
        sorted_tasks = task_manager.list_tasks(sort_by="priority")
        assert len(sorted_tasks) == 3
        # High priority should come first, then medium, then low
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"

        # Test sorting by ID
        sorted_tasks = task_manager.list_tasks(sort_by="id")
        assert len(sorted_tasks) == 3
        # Tasks should be in ascending ID order
        assert sorted_tasks[0].id == 1
        assert sorted_tasks[1].id == 2
        assert sorted_tasks[2].id == 3

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)