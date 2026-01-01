"""
TaskManager for the Todo App CLI.

This module defines the TaskManager class that handles task storage,
persistence, and business logic operations.
"""
import json
import os
from datetime import date, datetime
from typing import Dict, List, Optional
from .task import Task


class TaskManager:
    """
    Manages a collection of tasks with persistence to a JSON file.

    Attributes:
        tasks: Dictionary mapping task IDs to Task objects
        storage_path: Path to the JSON file for persistence
        next_id: The next ID to assign to a new task
    """

    def __init__(self, storage_path: str = "tasks.json"):
        """Initialize the TaskManager with a storage path."""
        self.storage_path = storage_path
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1
        self.load_tasks()

    def add_task(self, title: str, description: str = "", priority: str = "medium",
                 tags: List[str] = None, due_date: Optional[date] = None,
                 recurrence: str = "none") -> Task:
        """Create and add a new task to the collection."""
        if tags is None:
            tags = []

        # Create a new task with the next available ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )

        # Add the task to the collection
        self.tasks[task.id] = task
        self.next_id += 1

        # Update next_id to be one more than the highest ID
        if self.tasks:
            self.next_id = max(self.tasks.keys()) + 1

        # Save tasks to storage
        self.save_tasks()

        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: str = None, description: str = None,
                    status: str = None, priority: str = None, tags: List[str] = None,
                    due_date: Optional[date] = None, recurrence: str = None) -> Optional[Task]:
        """Update an existing task by its ID."""
        task = self.get_task(task_id)
        if not task:
            return None

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date
        if recurrence is not None:
            task.recurrence = recurrence

        # Save tasks to storage
        self.save_tasks()

        return task

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by its ID."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False

    def list_tasks(self, status: str = None, priority: str = None, sort_by: str = None) -> List[Task]:
        """Return a filtered and sorted list of tasks."""
        tasks = list(self.tasks.values())

        # Apply filters
        if status:
            tasks = [task for task in tasks if task.status == status]
        if priority:
            tasks = [task for task in tasks if task.priority == priority]

        # Apply sorting
        if sort_by == "due-date":
            tasks.sort(key=lambda x: (x.due_date is None, x.due_date))
        elif sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            tasks.sort(key=lambda x: priority_order.get(x.priority, 3))
        elif sort_by == "id":
            tasks.sort(key=lambda x: x.id)

        return tasks

    def search_tasks(self, query: str) -> List[Task]:
        """Return tasks that match the search query in title or description."""
        query = query.lower()
        matching_tasks = []

        for task in self.tasks.values():
            if (query in task.title.lower() or
                (task.description and query in task.description.lower()) or
                any(query in tag.lower() for tag in task.tags)):
                matching_tasks.append(task)

        return matching_tasks

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """Toggle the status of a task between pending and complete."""
        task = self.get_task(task_id)
        if not task:
            return None

        # If the task is recurring and is being marked as complete, create the next occurrence
        if task.is_recurring() and task.status == "pending":
            task.toggle_status()  # Mark current as complete
            self._create_next_occurrence(task)  # Create next occurrence
        else:
            task.toggle_status()  # Just toggle the status normally

        self.save_tasks()
        return task

    def _create_next_occurrence(self, completed_task: Task) -> Optional[Task]:
        """Create the next occurrence of a recurring task."""
        next_due_date = completed_task.get_next_occurrence_date()

        # Create a new task with the same properties but new due date
        new_task = Task(
            id=self.next_id,
            title=completed_task.title,
            description=completed_task.description,
            status="pending",  # New occurrence starts as pending
            priority=completed_task.priority,
            tags=completed_task.tags,
            due_date=next_due_date,
            recurrence=completed_task.recurrence,
            created_at=date.today()
        )

        # Add the new task to the collection
        self.tasks[new_task.id] = new_task
        self.next_id = max(self.tasks.keys()) + 1

        return new_task

    def get_tasks_due_soon(self, days: int = 1) -> List[Task]:
        """Get tasks that are due within the specified number of days."""
        due_soon_tasks = []
        target_date = date.today() + timedelta(days=days)

        for task in self.tasks.values():
            if task.due_date and date.today() <= task.due_date <= target_date and task.status == "pending":
                due_soon_tasks.append(task)

        return due_soon_tasks

    def load_tasks(self) -> None:
        """Load tasks from the storage file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Convert loaded data back to Task objects
                self.tasks = {}
                for task_data in data.get('tasks', []):
                    # Convert date strings back to date objects
                    due_date = None
                    if task_data.get('due_date'):
                        due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date()

                    created_at = None
                    if task_data.get('created_at'):
                        created_at = datetime.strptime(task_data['created_at'], '%Y-%m-%d').date()

                    task = Task(
                        id=task_data['id'],
                        title=task_data['title'],
                        description=task_data.get('description', ''),
                        status=task_data.get('status', 'pending'),
                        priority=task_data.get('priority', 'medium'),
                        tags=task_data.get('tags', []),
                        due_date=due_date,
                        recurrence=task_data.get('recurrence', 'none'),
                        created_at=created_at
                    )
                    self.tasks[task.id] = task

                # Set the next ID based on the highest existing ID
                if self.tasks:
                    self.next_id = max(self.tasks.keys()) + 1
                else:
                    self.next_id = 1

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error loading tasks from {self.storage_path}: {e}")
                self.tasks = {}
                self.next_id = 1
        else:
            # If file doesn't exist, start with empty tasks
            self.tasks = {}
            self.next_id = 1

    def save_tasks(self) -> None:
        """Save tasks to the storage file."""
        try:
            # Convert tasks to a serializable format
            tasks_data = []
            for task in self.tasks.values():
                task_dict = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'priority': task.priority,
                    'tags': task.tags,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'recurrence': task.recurrence,
                    'created_at': task.created_at.isoformat() if task.created_at else None
                }
                tasks_data.append(task_dict)

            # Write to file
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump({'tasks': tasks_data}, f, indent=2, ensure_ascii=False)

        except IOError as e:
            print(f"Error saving tasks to {self.storage_path}: {e}")