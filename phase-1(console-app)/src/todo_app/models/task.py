"""
Task model definition for the Todo App CLI.

This module defines the Task data class with all required fields and validation.
"""
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """
    Represents a single task in the todo application.

    Attributes:
        id: Unique identifier for the task
        title: Title of the task (required)
        description: Optional description of the task
        status: Current status of the task ("pending" or "complete")
        priority: Priority level ("high", "medium", "low")
        tags: List of tags associated with the task
        due_date: Due date for the task (optional)
        recurrence: Recurrence pattern ("daily", "weekly", "monthly", "none")
        created_at: Timestamp when the task was created
    """

    id: int
    title: str
    description: Optional[str] = ""
    status: str = "pending"
    priority: str = "medium"
    tags: List[str] = None
    due_date: Optional[date] = None
    recurrence: str = "none"
    created_at: date = None

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if self.tags is None:
            self.tags = []

        if self.created_at is None:
            self.created_at = date.today()

        # Validate required fields
        if not self.title or not self.title.strip():
            raise ValueError("Title is required and cannot be empty")

        # Validate title length
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        # Validate description length
        if self.description and len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Validate status
        if self.status not in ["pending", "complete"]:
            raise ValueError(f"Status must be 'pending' or 'complete', got '{self.status}'")

        # Validate priority
        if self.priority not in ["high", "medium", "low"]:
            raise ValueError(f"Priority must be 'high', 'medium', or 'low', got '{self.priority}'")

        # Validate tags
        if len(self.tags) > 10:
            raise ValueError("A task cannot have more than 10 tags")

        for tag in self.tags:
            self._validate_tag(tag)

        # Validate recurrence
        if self.recurrence not in ["daily", "weekly", "monthly", "none"]:
            raise ValueError(f"Recurrence must be 'daily', 'weekly', 'monthly', or 'none', got '{self.recurrence}'")

    def is_recurring(self) -> bool:
        """Check if the task is recurring."""
        return self.recurrence != "none"

    def get_next_occurrence_date(self, current_date: date = None) -> Optional[date]:
        """
        Calculate the next occurrence date based on the recurrence pattern.

        Args:
            current_date: The date from which to calculate the next occurrence.
                         Defaults to today if not provided.

        Returns:
            The next occurrence date or None if the task is not recurring
        """
        if not self.is_recurring():
            return None

        if current_date is None:
            current_date = date.today()

        if self.recurrence == "daily":
            return current_date + timedelta(days=1)
        elif self.recurrence == "weekly":
            return current_date + timedelta(weeks=1)
        elif self.recurrence == "monthly":
            # Calculate next month by adding 1 to the month
            if current_date.month == 12:
                next_month = 1
                next_year = current_date.year + 1
            else:
                next_month = current_date.month + 1
                next_year = current_date.year

            # Handle days that don't exist in some months (e.g., Jan 31 -> Feb 31 doesn't exist)
            try:
                return date(next_year, next_month, current_date.day)
            except ValueError:
                # If the day doesn't exist in the next month, use the last day of that month
                # For example, Jan 31 -> Feb 28 (or 29 in leap years)
                if next_month == 2:
                    # February - get the last day
                    if next_year % 4 == 0 and (next_year % 100 != 0 or next_year % 400 == 0):
                        # Leap year
                        return date(next_year, next_month, 29)
                    else:
                        # Non-leap year
                        return date(next_year, next_month, 28)
                elif next_month in [4, 6, 9, 11]:
                    # April, June, September, November have 30 days
                    return date(next_year, next_month, 30)
                else:
                    # All other months have 31 days
                    return date(next_year, next_month, 31)

    def _validate_tag(self, tag: str) -> None:
        """Validate a single tag."""
        if len(tag) > 50:
            raise ValueError(f"Tag '{tag}' exceeds 50 characters")

        # Check if tag is alphanumeric with optional hyphens/underscores
        for char in tag:
            if not (char.isalnum() or char in ['-', '_']):
                raise ValueError(f"Tag '{tag}' contains invalid character '{char}'. Tags must be alphanumeric with optional hyphens or underscores")

    def toggle_status(self) -> None:
        """Toggle the task status between pending and complete."""
        if self.status == "pending":
            self.status = "complete"
        else:
            self.status = "pending"