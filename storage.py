import json
import os
import tempfile

# tasks.json lives next to this file, regardless of where the program is run from
DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks(path=DEFAULT_PATH):
    """Return a list of task dicts. Returns [] if the file is missing,
    empty, or corrupted (the bad file is backed up as <path>.bak)."""
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
    except json.JSONDecodeError:
        _backup_corrupted(path)
        return []

    if not isinstance(data, list):
        _backup_corrupted(path)
        return []
    return data


def save_tasks(tasks, path=DEFAULT_PATH):
    """Write the list of task dicts to disk atomically, so a crash
    mid-write cannot corrupt the existing file."""
    directory = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def _backup_corrupted(path):
    try:
        os.replace(path, path + ".bak")
    except OSError:
        pass
