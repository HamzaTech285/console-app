"""
Validation utilities for the Todo App CLI.

This module provides functions for validating input data according to the specification.
"""
import re
from datetime import datetime, date
from typing import List, Optional


def validate_title(title: str) -> bool:
    """
    Validate a task title according to the specification.

    Args:
        title: The title to validate

    Returns:
        True if valid, False otherwise
    """
    if not title or not title.strip():
        return False
    if len(title) > 200:
        return False
    return True


def validate_description(description: str) -> bool:
    """
    Validate a task description according to the specification.

    Args:
        description: The description to validate

    Returns:
        True if valid, False otherwise
    """
    if description and len(description) > 1000:
        return False
    return True


def validate_status(status: str) -> bool:
    """
    Validate a task status according to the specification.

    Args:
        status: The status to validate

    Returns:
        True if valid, False otherwise
    """
    return status in ["pending", "complete"]


def validate_priority(priority: str) -> bool:
    """
    Validate a task priority according to the specification.

    Args:
        priority: The priority to validate

    Returns:
        True if valid, False otherwise
    """
    return priority in ["high", "medium", "low"]


def validate_tag(tag: str) -> bool:
    """
    Validate a single tag according to the specification.

    Args:
        tag: The tag to validate

    Returns:
        True if valid, False otherwise
    """
    if len(tag) > 50:
        return False

    # Check if tag is alphanumeric with optional hyphens/underscores
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', tag))


def validate_tags(tags: List[str]) -> bool:
    """
    Validate a list of tags according to the specification.

    Args:
        tags: The list of tags to validate

    Returns:
        True if valid, False otherwise
    """
    if len(tags) > 10:
        return False

    for tag in tags:
        if not validate_tag(tag):
            return False

    return True


def validate_recurrence(recurrence: str) -> bool:
    """
    Validate a recurrence pattern according to the specification.

    Args:
        recurrence: The recurrence to validate

    Returns:
        True if valid, False otherwise
    """
    return recurrence in ["daily", "weekly", "monthly", "none"]


def validate_date_format(date_str: str) -> bool:
    """
    Validate a date string in DD-MMM format (e.g., 05-Jan).

    Args:
        date_str: The date string to validate

    Returns:
        True if valid, False otherwise
    """
    if not date_str:
        return True  # Date can be optional

    try:
        # Check if the format is DD-MMM
        day, month = date_str.split('-')

        # Validate day is numeric and in range
        day_num = int(day)
        if day_num < 1 or day_num > 31:
            return False

        # Validate month is a valid 3-letter month abbreviation
        valid_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if month not in valid_months:
            return False

        return True
    except (ValueError, AttributeError):
        return False


def validate_date_edge_cases(date_str: str) -> List[str]:
    """
    Validate date strings for edge cases and return error messages.

    Args:
        date_str: The date string to validate

    Returns:
        List of error messages for edge cases
    """
    errors = []

    if not date_str:
        return errors  # Date can be optional

    try:
        day, month = date_str.split('-')

        # Validate day is numeric
        try:
            day_num = int(day)
        except ValueError:
            errors.append(f"Invalid day format in '{date_str}'. Day must be numeric.")
            return errors

        # Validate month
        valid_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if month not in valid_months:
            errors.append(f"Invalid month '{month}' in '{date_str}'. Must be a valid 3-letter month abbreviation (Jan, Feb, etc.).")
            return errors

        # Check for impossible dates
        if month in ['Feb'] and day_num > 29:
            errors.append(f"Invalid date '{date_str}'. February cannot have more than 29 days.")
        elif month in ['Feb'] and day_num == 29:
            # This would require checking for leap year, but we'll allow it since the actual date validation happens later
            pass
        elif month in ['Apr', 'Jun', 'Sep', 'Nov'] and day_num > 30:
            errors.append(f"Invalid date '{date_str}'. {month} cannot have more than 30 days.")
        elif day_num < 1 or day_num > 31:
            errors.append(f"Invalid day '{day_num}' in '{date_str}'. Day must be between 1 and 31.")

    except ValueError:
        errors.append(f"Invalid date format '{date_str}'. Expected format: DD-MMM (e.g., 05-Jan).")

    return errors


def parse_date_string(date_str: str) -> Optional[date]:
    """
    Parse a date string in DD-MMM format to a date object.
    Automatically assigns the nearest upcoming year.

    Args:
        date_str: The date string in DD-MMM format (e.g., 05-Jan)

    Returns:
        Date object or None if invalid
    """
    if not date_str:
        return None

    try:
        day, month = date_str.split('-')
        day_num = int(day)

        # Map month abbreviations to numbers
        month_map = {
            'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
        }

        if month not in month_map:
            return None

        month_num = month_map[month]

        # Determine the year (nearest upcoming year for the date)
        today = date.today()
        current_year = today.year

        # Create a date for this year
        target_date = date(current_year, month_num, day_num)

        # If the date has already passed this year, use next year
        if target_date < today:
            target_date = date(current_year + 1, month_num, day_num)

        return target_date
    except (ValueError, AttributeError):
        return None


def validate_task_data(title: str, description: str = "", status: str = "pending",
                      priority: str = "medium", tags: List[str] = None,
                      due_date: str = None, recurrence: str = "none") -> List[str]:
    """
    Validate all task data and return a list of validation errors.

    Args:
        title: Task title
        description: Task description
        status: Task status
        priority: Task priority
        tags: List of tags
        due_date: Due date string in DD-MMM format
        recurrence: Recurrence pattern

    Returns:
        List of validation error messages
    """
    if tags is None:
        tags = []

    errors = []

    if not validate_title(title):
        errors.append("Title is required and cannot exceed 200 characters")

    if not validate_description(description):
        errors.append("Description cannot exceed 1000 characters")

    if not validate_status(status):
        errors.append("Status must be 'pending' or 'complete'")

    if not validate_priority(priority):
        errors.append("Priority must be 'high', 'medium', or 'low'")

    if not validate_tags(tags):
        errors.append("Tags must be alphanumeric with optional hyphens/underscores, max 50 chars each, and max 10 tags total")

    if due_date and not validate_date_format(due_date):
        errors.append("Due date must be in DD-MMM format (e.g., 05-Jan)")

    if not validate_recurrence(recurrence):
        errors.append("Recurrence must be 'daily', 'weekly', 'monthly', or 'none'")

    return errors