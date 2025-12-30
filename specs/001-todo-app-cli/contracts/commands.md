# CLI Command Contracts: Todo App

## Command Interface

### Add Command
- **Signature**: `todo add <title> [description] [options]`
- **Options**:
  - `--priority`: high|medium|low (default: medium)
  - `--tags`: comma-separated tags (alphanumeric with hyphens/underscores)
  - `--due-date`: DD-MMM format (e.g., 05-Jan)
  - `--recurring`: daily|weekly|monthly
- **Output**: Success message with assigned task ID
- **Error codes**: 1 for validation errors, 2 for storage errors

### List Command
- **Signature**: `todo list [options]`
- **Options**:
  - `--status`: pending|complete
  - `--priority`: high|medium|low
  - `--sort`: due-date|priority|id
- **Output**: Formatted list of tasks with ID, title, status, priority, due date
- **Error codes**: 1 for storage errors

### Update Command
- **Signature**: `todo update <id> [options]`
- **Options**:
  - `--title`: new title
  - `--description`: new description
  - `--priority`: high|medium|low
  - `--tags`: comma-separated tags
  - `--due-date`: DD-MMM format
- **Output**: Success message
- **Error codes**: 1 for validation errors, 2 for not found, 3 for storage errors

### Delete Command
- **Signature**: `todo delete <id>`
- **Output**: Success message
- **Error codes**: 1 for not found, 2 for storage errors

### Toggle Command
- **Signature**: `todo toggle <id>`
- **Output**: Success message with new status
- **Error codes**: 1 for not found, 2 for storage errors

### Search Command
- **Signature**: `todo search <query>`
- **Output**: Formatted list of matching tasks
- **Error codes**: 1 for storage errors