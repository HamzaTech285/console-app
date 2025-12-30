"""
CLI command implementations for the Todo App CLI.

This module contains the functions that implement each CLI command.
"""
from typing import List
from ..models.task_manager import TaskManager
from ..utils.validators import parse_date_string, validate_task_data


def add_task(args, task_manager: TaskManager):
    """
    Add a new task.

    Args:
        args: Parsed command-line arguments
        task_manager: TaskManager instance to use
    """
    # Parse due date if provided
    due_date = None
    if args.due_date:
        due_date = parse_date_string(args.due_date)
        if due_date is None:
            print(f"Error: Invalid date format '{args.due_date}'. Use DD-MMM format (e.g., 05-Jan)")
            return

    # Validate task data
    errors = validate_task_data(
        title=args.title,
        description=args.description,
        priority=args.priority,
        tags=args.tags or [],
        due_date=args.due_date,
        recurrence=args.recurring or "none"
    )

    if errors:
        for error in errors:
            print(f"Error: {error}")
        return

    try:
        task = task_manager.add_task(
            title=args.title,
            description=args.description,
            priority=args.priority,
            tags=args.tags or [],
            due_date=due_date,
            recurrence=args.recurring or "none"
        )
        print(f"Task added successfully with ID: {task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def list_tasks(args, task_manager: TaskManager):
    """
    List all tasks with optional filtering and sorting.

    Args:
        args: Parsed command-line arguments
        task_manager: TaskManager instance to use
    """
    tasks = task_manager.list_tasks(
        status=args.status,
        priority=args.priority,
        sort_by=args.sort
    )

    if not tasks:
        print("No tasks found.")
        return

    # Print header
    print(f"{'ID':<4} {'Status':<10} {'Priority':<10} {'Title':<30} {'Due Date':<12} {'Tags'}")

    # Print each task
    for task in tasks:
        due_date_str = task.due_date.strftime('%d-%b') if task.due_date else 'None'
        tags_str = ', '.join(task.tags) if task.tags else ''
        print(f"{task.id:<4} {task.status:<10} {task.priority:<10} {task.title[:30]:<30} {due_date_str:<12} {tags_str}")


def update_task(args, task_manager: TaskManager):
    """
    Update an existing task.

    Args:
        args: Parsed command-line arguments
        task_manager: TaskManager instance to use
    """
    # Parse due date if provided
    due_date = None
    if args.due_date:
        due_date = parse_date_string(args.due_date)
        if due_date is None:
            print(f"Error: Invalid date format '{args.due_date}'. Use DD-MMM format (e.g., 05-Jan)")
            return

    # Prepare update parameters
    update_params = {}
    if args.title is not None:
        update_params['title'] = args.title
    if args.description is not None:
        update_params['description'] = args.description
    if args.status is not None:
        update_params['status'] = args.status
    if args.priority is not None:
        update_params['priority'] = args.priority
    if args.tags is not None:
        update_params['tags'] = args.tags
    if args.due_date is not None:
        update_params['due_date'] = due_date

    # Validate task data if any field is being updated
    if update_params:
        # Get current task to use existing values for validation
        current_task = task_manager.get_task(args.id)
        if not current_task:
            print(f"Error: Task with ID {args.id} not found")
            return

        # Use new values if provided, otherwise use current values
        title = update_params.get('title', current_task.title)
        description = update_params.get('description', current_task.description)
        status = update_params.get('status', current_task.status)
        priority = update_params.get('priority', current_task.priority)
        tags = update_params.get('tags', current_task.tags)
        due_date_str = args.due_date  # Only pass the string if it was provided in args

        errors = validate_task_data(
            title=title,
            description=description,
            status=status,
            priority=priority,
            tags=tags,
            due_date=due_date_str if args.due_date else None
        )

        if errors:
            for error in errors:
                print(f"Error: {error}")
            return

    task = task_manager.update_task(args.id, **update_params)
    if task:
        print(f"Task {args.id} updated successfully")
    else:
        print(f"Error: Task with ID {args.id} not found")


def delete_task(args, task_manager: TaskManager):
    """
    Delete a task.

    Args:
        args: Parsed command-line arguments
        task_manager: TaskManager instance to use
    """
    success = task_manager.delete_task(args.id)
    if success:
        print(f"Task {args.id} deleted successfully")
    else:
        print(f"Error: Task with ID {args.id} not found")


def toggle_task(args, task_manager: TaskManager):
    """
    Toggle task status between pending and complete.

    Args:
        args: Parsed command-line arguments
        task_manager: TaskManager instance to use
    """
    task = task_manager.toggle_task_status(args.id)
    if task:
        print(f"Task {args.id} status toggled to {task.status}")
    else:
        print(f"Error: Task with ID {args.id} not found")


def search_tasks(args, task_manager: TaskManager):
    """
    Search tasks by keyword.

    Args:
        args: Parsed command-line arguments
        task_manager: TaskManager instance to use
    """
    tasks = task_manager.search_tasks(args.query)

    if not tasks:
        print("No matching tasks found.")
        return

    # Print header
    print(f"{'ID':<4} {'Status':<10} {'Priority':<10} {'Title':<30} {'Due Date':<12} {'Tags'}")

    # Print each task
    for task in tasks:
        due_date_str = task.due_date.strftime('%d-%b') if task.due_date else 'None'
        tags_str = ', '.join(task.tags) if task.tags else ''
        print(f"{task.id:<4} {task.status:<10} {task.priority:<10} {task.title[:30]:<30} {due_date_str:<12} {tags_str}")