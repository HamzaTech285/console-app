# Quickstart: Todo App CLI

## Prerequisites
- Python 3.13+
- `uv` package manager

## Setup

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Usage

### Adding Tasks
```bash
todo add "Task title" "Optional description"
todo add "Buy groceries" "Milk, bread, eggs" --priority high --tags "shopping,urgent"
```

### Listing Tasks
```bash
todo list
todo list --status pending
todo list --priority high
todo list --sort due-date
todo list --sort priority
```

### Updating Tasks
```bash
todo update 1 --title "New title"
todo update 1 --description "New description"
todo update 1 --priority low
todo update 1 --tags "work,meeting"
```

### Deleting Tasks
```bash
todo delete 1
```

### Toggling Task Status
```bash
todo toggle 1
```

### Searching Tasks
```bash
todo search "groceries"
```

### Adding Recurring Tasks
```bash
todo add "Take medication" --recurring daily
todo add "Team meeting" --recurring weekly
```

### Setting Due Dates
```bash
todo add "Project deadline" --due-date 15-Mar
```

## Development

### Running Tests
```bash
uv run pytest
```

### Running the Application
```bash
uv run python -m src.todo_app.main
```

### Code Quality
```bash
uv run flake8 src/
uv run black src/
```