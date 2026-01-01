"""
Main entry point for the Todo App CLI.

This module provides the main function that runs the CLI application.
"""
from .cli.parsers import parse_arguments, process_parsed_args
from .cli.commands import add_task, list_tasks, update_task, delete_task, toggle_task, search_tasks
from .models.task_manager import TaskManager


def main():
    """
    Main function for the todo CLI application.
    Parses arguments and executes the appropriate command.
    """
    # Parse command-line arguments
    args = parse_arguments()
    args = process_parsed_args(args)

    # Create task manager instance
    task_manager = TaskManager()

    # Execute the appropriate command based on the parsed arguments
    try:
        if args.command == 'add':
            add_task(args, task_manager)
        elif args.command == 'list':
            list_tasks(args, task_manager)
        elif args.command == 'update':
            update_task(args, task_manager)
        elif args.command == 'delete':
            delete_task(args, task_manager)
        elif args.command == 'toggle':
            toggle_task(args, task_manager)
        elif args.command == 'search':
            search_tasks(args, task_manager)
        else:
            # This should not happen due to argparse validation
            print(f"Unknown command: {args.command}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()