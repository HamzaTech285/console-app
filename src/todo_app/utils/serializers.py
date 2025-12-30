"""
Serialization utilities for the Todo App CLI.

This module provides functions for converting Task objects to and from JSON format.
"""
import json
from datetime import date, datetime
from typing import Any, Dict
from ..models.task import Task


def serialize_task(task: Task) -> Dict[str, Any]:
    """
    Serialize a Task object to a dictionary format suitable for JSON storage.

    Args:
        task: The Task object to serialize

    Returns:
        Dictionary representation of the Task
    """
    return {
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


def deserialize_task(data: Dict[str, Any]) -> Task:
    """
    Deserialize a dictionary to a Task object.

    Args:
        data: Dictionary containing task data

    Returns:
        Task object created from the dictionary data
    """
    # Convert date strings back to date objects
    due_date = None
    if data.get('due_date'):
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()

    created_at = None
    if data.get('created_at'):
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%d').date()

    return Task(
        id=data['id'],
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        tags=data.get('tags', []),
        due_date=due_date,
        recurrence=data.get('recurrence', 'none'),
        created_at=created_at
    )


class TaskEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for Task objects and date objects.
    """
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Task):
            return serialize_task(obj)
        return super().default(obj)


def save_tasks_to_json(tasks, filepath: str) -> None:
    """
    Save a collection of tasks to a JSON file.

    Args:
        tasks: Collection of Task objects or dictionary representations
        filepath: Path to the JSON file to save to
    """
    tasks_data = []
    for task in tasks:
        if isinstance(task, Task):
            tasks_data.append(serialize_task(task))
        else:
            tasks_data.append(task)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({'tasks': tasks_data}, f, indent=2, ensure_ascii=False, cls=TaskEncoder)


def load_tasks_from_json(filepath: str):
    """
    Load tasks from a JSON file.

    Args:
        filepath: Path to the JSON file to load from

    Returns:
        List of Task objects
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tasks = []
    for task_data in data.get('tasks', []):
        task = deserialize_task(task_data)
        tasks.append(task)

    return tasks