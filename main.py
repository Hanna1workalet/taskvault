import storage
from tasks import TaskManager, PRIORITIES

MENU = """
========== TaskVault ==========
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
==============================="""


def print_tasks(tasks, title):
    print(f"\n--- {title} ---")
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(task)


def ask_task_id(prompt="Enter task id: "):
    raw = input(prompt).strip()
    if not raw.isdigit():
        raise ValueError("Task id must be a number")
    return int(raw)


def ask_priority(default="medium"):
    raw = input(f"Priority ({'/'.join(PRIORITIES)}): ").strip()
    return raw or default


def handle_add(manager):
    title = input("Task title: ")
    priority = ask_priority()
    task = manager.add_task(title, priority)
    print(f"Added: {task}")
    return True


def handle_complete(manager):
    task = manager.complete_task(ask_task_id())
    print(f"Completed: {task}")
    return True


def handle_uncomplete(manager):
    task = manager.uncomplete_task(ask_task_id())
    print(f"Reopened: {task}")
    return True


def handle_set_priority(manager):
    task_id = ask_task_id()
    task = manager.set_priority(task_id, ask_priority())
    print(f"Updated: {task}")
    return True


def handle_delete(manager):
    task_id = ask_task_id()
    task = manager.get_task(task_id)
    confirm = input(f"Delete '{task.title}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return False
    manager.delete_task(task_id)
    print("Deleted.")
    return True


def main():
    manager = TaskManager.from_dicts(storage.load_tasks())
    print(f"Loaded {len(manager.tasks)} task(s).")

    # Actions that modify data return True so the caller knows to save.
    actions = {
        "1": handle_add,
        "6": handle_complete,
        "7": handle_uncomplete,
        "8": handle_set_priority,
        "9": handle_delete,
    }

    while True:
        print(MENU)
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        try:
            if choice in actions:
                if actions[choice](manager):
                    storage.save_tasks(manager.to_dicts())
            elif choice == "2":
                print_tasks(manager.list_tasks("all"), "All tasks")
            elif choice == "3":
                print_tasks(manager.list_tasks("pending"), "Pending tasks")
            elif choice == "4":
                print_tasks(manager.list_tasks("done"), "Completed tasks")
            elif choice == "5":
                print_tasks(
                    manager.list_tasks("all", sort_by_priority=True),
                    "Tasks by priority",
                )
            else:
                print("Invalid option. Choose a number from 0 to 9.")
        except (ValueError, KeyError) as e:
            print(f"Error: {e.args[0]}")
        except OSError as e:
            print(f"Could not save tasks: {e}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")