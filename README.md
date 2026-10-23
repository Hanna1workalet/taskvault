# TaskVault

A personal command-line task manager in Python. Create tasks, assign priorities, track completion, and keep your tasks after closing the program.

## Features

- Add tasks with a priority (`low`, `medium`, `high`)
- Mark tasks as complete or incomplete
- Change a task's priority
- Delete tasks (with confirmation)
- View all, pending, or completed tasks
- View tasks sorted by priority
- Automatic saving to `tasks.json`

## Project Structure

```
taskvault/
├── main.py       # Command-line menu and program loop
├── tasks.py      # Task model and TaskManager logic
├── storage.py    # Loading and saving tasks.json
├── tasks.json    # Saved tasks (created on first save)
└── README.md
```

| File | Responsibility |
|---|---|
| `main.py` | Shows the menu, reads input, calls `TaskManager`, saves after changes |
| `tasks.py` | `Task` dataclass and `TaskManager` (add, complete, delete, filter, sort) |
| `storage.py` | `load_tasks()` and `save_tasks()` using JSON |

`tasks.py` does no file I/O. `storage.py` only reads and writes plain dicts. `main.py` connects the two.

## Requirements

- Python 3.7 or newer
- No external packages

## Usage

```
cd taskvault
python main.py
```

### Menu

```
1. Add task
2. View all tasks
3. View pending tasks
4. View completed tasks
5. View tasks by priority
6. Mark task as complete
7. Mark task as incomplete
8. Change task priority
9. Delete task
0. Exit
```

### Example Session

```
Select an option: 1
Task title: Finish report
Priority (low/medium/high) [medium]: high
Added:   1. [ ] Finish report (high)

Select an option: 6
Enter task id: 1
Completed:   1. [x] Finish report (high)
```

Task display format: `id. [status] title (priority)`, where `[ ]` is pending and `[x]` is complete.

## Data Storage

Tasks are saved to `tasks.json` in the same folder as the program, no matter where you run it from. Each task looks like this:

```json
{
  "id": 1,
  "title": "Finish report",
  "priority": "high",
  "completed": false,
  "created_at": "2026-10-23 14:30"
}
```

- Tasks are saved after every change (add, complete, reopen, priority change, delete).
- Saving is atomic: data is written to a temporary file and then swapped in, so a crash cannot corrupt your tasks.
- If `tasks.json` is corrupted, it is renamed to `tasks.json.bak` and the program starts with an empty list.

## Error Handling

| Situation | Result |
|---|---|
| Empty title | `Error: Title cannot be empty` |
| Invalid priority | `Error: Priority must be one of: low, medium, high` |
| Unknown task id | `Error: No task with id <n>` |
| Non-numeric id | `Error: Task id must be a number` |
| Ctrl+C / Ctrl+D | Exits cleanly |

## Possible Improvements

- Due dates and reminders
- Search by keyword
- Edit task titles
- Categories or tags
- Unit tests for `tasks.py` and `storage.py`