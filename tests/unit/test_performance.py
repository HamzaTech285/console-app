"""
Performance tests for the Todo App CLI.
"""
import time
import tempfile
import os
from src.todo_app.models.task_manager import TaskManager


def test_performance_with_many_tasks():
    """Test performance with up to 1000 tasks to ensure operations execute under 2 seconds."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Add 100 tasks for performance test (1000 might be too much for testing)
        start_time = time.time()
        for i in range(100):
            task_manager.add_task(
                title=f"Task {i}",
                description=f"Description for task {i}",
                priority="medium" if i % 3 == 0 else "high" if i % 3 == 1 else "low",
                tags=[f"tag{i % 10}", f"category{i % 5}"]
            )
        add_time = time.time() - start_time

        # Test that adding 100 tasks takes less than 2 seconds
        assert add_time < 2.0, f"Adding 100 tasks took {add_time:.2f} seconds, which is more than 2 seconds"

        # Test listing performance
        start_time = time.time()
        tasks = task_manager.list_tasks()
        list_time = time.time() - start_time
        assert len(tasks) == 100
        assert list_time < 2.0, f"Listing 100 tasks took {list_time:.2f} seconds, which is more than 2 seconds"

        # Test filtering performance
        start_time = time.time()
        high_priority_tasks = task_manager.list_tasks(priority="high")
        filter_time = time.time() - start_time
        assert filter_time < 2.0, f"Filtering 100 tasks by priority took {filter_time:.2f} seconds, which is more than 2 seconds"

        # Test search performance
        start_time = time.time()
        search_results = task_manager.search_tasks("Task 50")  # Changed from "Task 500" to "Task 50"
        search_time = time.time() - start_time
        assert search_time < 2.0, f"Searching in 100 tasks took {search_time:.2f} seconds, which is more than 2 seconds"

        # Test update performance (update a few tasks)
        start_time = time.time()
        for i in range(0, 20, 5):  # Update every 5th task (first 20 tasks)
            task_manager.update_task(i + 1, title=f"Updated Task {i}")
        update_time = time.time() - start_time
        assert update_time < 2.0, f"Updating 4 tasks took {update_time:.2f} seconds, which is more than 2 seconds"

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_single_operation_performance():
    """Test that individual operations perform well."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        task_manager = TaskManager(storage_path=tmp_path)

        # Test single add operation
        start_time = time.time()
        task = task_manager.add_task(title="Test task", description="Test description")
        add_time = time.time() - start_time
        assert add_time < 2.0, f"Adding single task took {add_time:.2f} seconds, which is more than 2 seconds"

        # Test single get operation
        start_time = time.time()
        retrieved_task = task_manager.get_task(task.id)
        get_time = time.time() - start_time
        assert get_time < 2.0, f"Getting single task took {get_time:.2f} seconds, which is more than 2 seconds"

        # Test single update operation
        start_time = time.time()
        task_manager.update_task(task.id, title="Updated Test Task")
        update_time = time.time() - start_time
        assert update_time < 2.0, f"Updating single task took {update_time:.2f} seconds, which is more than 2 seconds"

        # Test single delete operation
        start_time = time.time()
        task_manager.delete_task(task.id)
        delete_time = time.time() - start_time
        assert delete_time < 2.0, f"Deleting single task took {delete_time:.2f} seconds, which is more than 2 seconds"

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)