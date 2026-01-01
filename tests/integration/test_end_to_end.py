"""
Integration tests for end-to-end user workflows.
"""
import tempfile
import os
from src.todo_app.models.task_manager import TaskManager


def test_complete_workflow():
    """Test a complete user workflow: add, list, update, toggle, search, delete."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Initialize task manager
        task_manager = TaskManager(storage_path=tmp_path)

        # 1. Add multiple tasks
        task1 = task_manager.add_task(
            title="Buy groceries",
            description="Milk, bread, eggs",
            priority="high",
            tags=["shopping", "urgent"],
            due_date=None
        )

        task2 = task_manager.add_task(
            title="Finish report",
            description="Complete quarterly report",
            priority="medium",
            tags=["work"],
            due_date=None
        )

        # 2. List all tasks
        all_tasks = task_manager.list_tasks()
        assert len(all_tasks) == 2

        # 3. Filter tasks by priority
        high_priority_tasks = task_manager.list_tasks(priority="high")
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].id == task1.id

        # 4. Update a task
        updated_task = task_manager.update_task(
            task_id=task2.id,
            title="Finished report",
            priority="low"
        )
        assert updated_task is not None
        assert updated_task.title == "Finished report"
        assert updated_task.priority == "low"

        # 5. Toggle task status
        toggled_task = task_manager.toggle_task_status(task1.id)
        assert toggled_task is not None
        assert toggled_task.status == "complete"

        # 6. Search for tasks
        search_results = task_manager.search_tasks("groceries")
        assert len(search_results) == 1
        assert search_results[0].id == task1.id

        # 7. Verify the final state
        all_tasks = task_manager.list_tasks()
        assert len(all_tasks) == 2

        # Verify specific task states
        retrieved_task1 = task_manager.get_task(task1.id)
        assert retrieved_task1.status == "complete"
        assert retrieved_task1.title == "Buy groceries"

        retrieved_task2 = task_manager.get_task(task2.id)
        assert retrieved_task2.title == "Finished report"
        assert retrieved_task2.priority == "low"

        # 8. Delete a task
        delete_result = task_manager.delete_task(task1.id)
        assert delete_result is True

        # 9. Verify deletion
        all_tasks = task_manager.list_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == task2.id

        # 10. Try to get the deleted task (should return None)
        deleted_task = task_manager.get_task(task1.id)
        assert deleted_task is None

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_recurring_task_workflow():
    """Test the complete workflow for recurring tasks."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Initialize task manager
        task_manager = TaskManager(storage_path=tmp_path)

        # 1. Add a recurring task
        recurring_task = task_manager.add_task(
            title="Take medication",
            description="Daily vitamin supplements",
            priority="high",
            tags=["health"],
            recurrence="daily"
        )

        # 2. Verify the task was created
        assert recurring_task.recurrence == "daily"
        assert recurring_task.status == "pending"

        # 3. Toggle the recurring task to complete (this should create a new occurrence)
        toggled_task = task_manager.toggle_task_status(recurring_task.id)
        assert toggled_task.status == "complete"

        # 4. List all tasks - should include the completed task and a new occurrence
        all_tasks = task_manager.list_tasks()
        assert len(all_tasks) == 2  # Original completed + new occurrence

        # 5. Find the new occurrence (should have same title but different ID and pending status)
        new_occurrence = None
        completed_task = None
        for task in all_tasks:
            if task.title == "Take medication":
                if task.status == "pending" and task.id != recurring_task.id:
                    new_occurrence = task
                elif task.status == "complete" and task.id == recurring_task.id:
                    completed_task = task

        assert new_occurrence is not None
        assert completed_task is not None
        assert new_occurrence.status == "pending"
        assert completed_task.status == "complete"
        assert new_occurrence.id != completed_task.id

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_persistence_workflow():
    """Test that tasks are properly saved and loaded."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        # Create first task manager and add tasks
        task_manager1 = TaskManager(storage_path=tmp_path)

        task1 = task_manager1.add_task(
            title="Task 1",
            description="First task",
            priority="high"
        )

        task2 = task_manager1.add_task(
            title="Task 2",
            description="Second task",
            priority="low"
        )

        # Close the first manager (data should be saved)
        del task_manager1

        # Create a new task manager with the same storage path
        task_manager2 = TaskManager(storage_path=tmp_path)

        # Verify that tasks were loaded correctly
        all_tasks = task_manager2.list_tasks()
        assert len(all_tasks) == 2

        # Verify specific task data
        loaded_task1 = task_manager2.get_task(task1.id)
        assert loaded_task1 is not None
        assert loaded_task1.title == "Task 1"
        assert loaded_task1.description == "First task"
        assert loaded_task1.priority == "high"

        loaded_task2 = task_manager2.get_task(task2.id)
        assert loaded_task2 is not None
        assert loaded_task2.title == "Task 2"
        assert loaded_task2.description == "Second task"
        assert loaded_task2.priority == "low"

        # Add another task with the new manager
        task3 = task_manager2.add_task(
            title="Task 3",
            priority="medium"
        )

        # Close the second manager
        del task_manager2

        # Create a third manager to verify all tasks are loaded
        task_manager3 = TaskManager(storage_path=tmp_path)
        all_tasks = task_manager3.list_tasks()
        assert len(all_tasks) == 3

        # Verify all three tasks exist
        assert task_manager3.get_task(task1.id) is not None
        assert task_manager3.get_task(task2.id) is not None
        assert task_manager3.get_task(task3.id) is not None

    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.remove(tmp_path)