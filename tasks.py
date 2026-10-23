from dataclasses import dataclass, field, asdict
from datetime import datetime

PRIORITIES = ("low", "medium", "high")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    completed: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=int(data["id"]),
            title=data["title"],
            priority=data.get("priority", "medium"),
            completed=bool(data.get("completed", False)),
            created_at=data.get("created_at", ""),
        )

    def __str__(self):
        mark = "[x]" if self.completed else "[ ]"
        return f"{self.id:>3}. {mark} {self.title} ({self.priority})"


class TaskManager:
    def __init__(self, tasks=None):
        self.tasks = tasks or []

    # ---------- helpers ----------
    def _next_id(self):
        return max((t.id for t in self.tasks), default=0) + 1

    @staticmethod
    def _validate_priority(priority):
        priority = priority.strip().lower()
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(PRIORITIES)}")
        return priority

    def get_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task with id {task_id}")

    # ---------- operations ----------
    def add_task(self, title, priority="medium"):
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")
        task = Task(
            id=self._next_id(),
            title=title,
            priority=self._validate_priority(priority),
        )
        self.tasks.append(task)
        return task

    def complete_task(self, task_id):
        task = self.get_task(task_id)
        task.completed = True
        return task

    def uncomplete_task(self, task_id):
        task = self.get_task(task_id)
        task.completed = False
        return task

    def set_priority(self, task_id, priority):
        task = self.get_task(task_id)
        task.priority = self._validate_priority(priority)
        return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        self.tasks.remove(task)
        return task

    def list_tasks(self, status="all", sort_by_priority=False):
        """status: 'all', 'pending', or 'done'."""
        if status == "pending":
            result = [t for t in self.tasks if not t.completed]
        elif status == "done":
            result = [t for t in self.tasks if t.completed]
        elif status == "all":
            result = list(self.tasks)
        else:
            raise ValueError("Status must be 'all', 'pending', or 'done'")

        if sort_by_priority:
            result.sort(key=lambda t: (PRIORITY_ORDER[t.priority], t.id))
        return result

    # ---------- serialization (used by storage.py) ----------
    def to_dicts(self):
        return [t.to_dict() for t in self.tasks]

    @classmethod
    def from_dicts(cls, data):
        return cls([Task.from_dict(d) for d in data])