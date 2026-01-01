# Data Model: Todo App CLI

## Task Entity

### Fields
- **id**: Integer (auto-incrementing, unique identifier)
- **title**: String (required, max 200 characters)
- **description**: String (optional, max 1000 characters)
- **status**: String (enum: "pending", "complete", default: "pending")
- **priority**: String (enum: "high", "medium", "low", default: "medium")
- **tags**: List of Strings (alphanumeric with hyphens/underscores, case-insensitive, max 10 tags)
- **due_date**: Date object (stored as datetime.date, input in DD-MMM format)
- **recurrence**: String (enum: "daily", "weekly", "monthly", "none", default: "none")
- **created_at**: DateTime (timestamp when task was created)

### Validation Rules
- ID must be unique across all tasks
- Title is required and must not be empty
- Title and description must not exceed character limits
- Status must be one of the allowed values ("pending", "complete")
- Priority must be one of the allowed values ("high", "medium", "low")
- Each tag must be alphanumeric with optional hyphens/underscores, max 50 chars each
- Due date, if provided, must be a valid date object
- Recurrence must be one of the allowed values or "none"

### State Transitions
- Status can transition from "pending" to "complete" and vice versa
- All other fields remain mutable except for ID

## TaskManager Entity

### Fields
- **tasks**: List of Task objects (the collection of all tasks)
- **storage_path**: String (path to the JSON file for persistence)

### Methods
- **add_task**: Creates a new task and adds it to the collection
- **get_task**: Retrieves a task by ID
- **update_task**: Modifies an existing task by ID
- **delete_task**: Removes a task by ID
- **list_tasks**: Returns filtered/sorted list of tasks
- **search_tasks**: Returns tasks matching search criteria
- **load_tasks**: Loads tasks from storage file
- **save_tasks**: Saves tasks to storage file