import argparse
from datetime import datetime
from .utils import load_tasks, save_tasks, get_next_id


def handle_add(args):
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "text": args.text,
        "created": datetime.now().isoformat(),
        "module": args.module or "general",
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: [{new_task['id']}] {new_task['text']}")


def handle_list(args):
    tasks = load_tasks()
    if args.module:
        tasks = [t for t in tasks if t["module"] == args.module]
    for task in tasks:
        print(f"[{task['id']}] ({task['module']}) {task['text']}")


def handle_remove(args):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != args.id]
    save_tasks(tasks)
    print(f"Task {args.id} removed (if it existed).")


def run_cli():
    parser = argparse.ArgumentParser(
        prog="lisa", description="Local Intelligent Scheduling Assistant (LISA)"
    )
    subparsers = parser.add_subparsers(title="commands")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", type=str, help="Task description")
    add_parser.add_argument(
        "--module", type=str, help="Task module (e.g., work, home, study)"
    )
    add_parser.set_defaults(func=handle_add)

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--module", type=str, help="Filter by module")
    list_parser.set_defaults(func=handle_list)

    remove_parser = subparsers.add_parser("remove", help="Remove a task by ID")
    remove_parser.add_argument("id", type=int, help="Task ID to remove")
    remove_parser.set_defaults(func=handle_remove)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
