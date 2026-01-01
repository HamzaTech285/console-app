"""
Argument parsers for the Todo App CLI.

This module defines the command-line argument parsers using argparse.
"""
import argparse
from typing import Any


def create_parser() -> argparse.ArgumentParser:
    """
    Create the main argument parser for the todo CLI application.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog='todo',
        description='A command-line todo application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  todo add "Buy groceries" "Milk, bread, eggs" --priority high --tags "shopping,urgent"
  todo list
  todo list --status pending
  todo list --priority high
  todo list --sort due-date
  todo update 1 --title "New title" --priority low
  todo delete 1
  todo toggle 1
  todo search "groceries"
        """.strip()
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=True)

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Title of the task')
    add_parser.add_argument('description', nargs='?', default='', help='Description of the task')
    add_parser.add_argument('--priority', choices=['high', 'medium', 'low'], default='medium',
                           help='Priority level (default: medium)')
    add_parser.add_argument('--tags', help='Comma-separated tags (alphanumeric with hyphens/underscores)')
    add_parser.add_argument('--due-date', help='Due date in DD-MMM format (e.g., 05-Jan)')
    add_parser.add_argument('--recurring', choices=['daily', 'weekly', 'monthly'], help='Recurring pattern')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', choices=['pending', 'complete'], help='Filter by status')
    list_parser.add_argument('--priority', choices=['high', 'medium', 'low'], help='Filter by priority')
    list_parser.add_argument('--sort', choices=['due-date', 'priority', 'id'], help='Sort by criteria')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID to update')
    update_parser.add_argument('--title', help='New title')
    update_parser.add_argument('--description', help='New description')
    update_parser.add_argument('--status', choices=['pending', 'complete'], help='New status')
    update_parser.add_argument('--priority', choices=['high', 'medium', 'low'], help='New priority')
    update_parser.add_argument('--tags', help='New comma-separated tags')
    update_parser.add_argument('--due-date', help='New due date in DD-MMM format (e.g., 05-Jan)')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID to delete')

    # Toggle command
    toggle_parser = subparsers.add_parser('toggle', help='Toggle task status')
    toggle_parser.add_argument('id', type=int, help='Task ID to toggle')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks by keyword')
    search_parser.add_argument('query', help='Search query')

    return parser


def parse_arguments(args: Any = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Arguments to parse (defaults to sys.argv)

    Returns:
        Parsed arguments namespace
    """
    parser = create_parser()
    return parser.parse_args(args)


def process_parsed_args(args: argparse.Namespace) -> argparse.Namespace:
    """
    Process parsed arguments to handle any special formatting.

    Args:
        args: Parsed arguments namespace

    Returns:
        Processed arguments namespace
    """
    # Process tags from comma-separated string to list
    if hasattr(args, 'tags') and args.tags:
        args.tags = [tag.strip() for tag in args.tags.split(',') if tag.strip()]
    elif hasattr(args, 'tags') and args.tags == '':
        args.tags = []

    return args