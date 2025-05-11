import argparse
import argcomplete
from datetime import datetime
from .utils import (
    load_tasks, save_tasks, get_next_id, log_action,
    VALID_MODULES, PRIORITY_LEVELS,
    export_tasks, import_tasks, clear_tasks
)

def handle_add(args):
    tasks = load_tasks()
    text = args.text.strip()
    if not text:
        print("Error: Task description cannot be empty.")
        return

    if args.module not in VALID_MODULES:
        print(f"Error: Invalid module. Choose from: {', '.join(VALID_MODULES)}")
        return

    if any(t['text'] == text and t['module'] == args.module for t in tasks) and not args.force:
        print("Error: Duplicate task exists. Use --force to override.")
        return

    try:
        due_date = args.due if args.due else None
        if due_date:
            datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid due date format. Use YYYY-MM-DD.")
        return

    if args.priority and args.priority not in PRIORITY_LEVELS:
        print(f"Error: Invalid priority. Choose from: {', '.join(PRIORITY_LEVELS)}")
        return

    new_task = {
        "id": get_next_id(tasks),
        "text": text,
        "created": datetime.now().isoformat(),
        "module": args.module,
        "due": due_date,
        "priority": args.priority or "medium"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    log_action(f"Added task {new_task['id']}: {text} [{args.module}]")
    print(f"✅ Task added: [{new_task['id']}] {text}")

def handle_list(args):
    tasks = load_tasks()
    if args.module:
        tasks = [t for t in tasks if t['module'] == args.module]
    tasks.sort(key=lambda x: (x.get("due") or "", x["id"]))
    for task in tasks:
        print(f"[{task['id']}] ({task['module']}) {task['text']} | Due: {task.get('due', '-')} | Priority: {task.get('priority', '-')}")
    log_action("Listed tasks")

def handle_remove(args):
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t['id'] != args.id]
    if len(tasks) == before:
        print(f"⚠️ Task ID {args.id} not found.")
    else:
        print(f"🗑️ Task {args.id} removed.")
        log_action(f"Removed task {args.id}")
    save_tasks(tasks)

def handle_clear(args):
    confirm = input("Are you sure you want to delete all tasks? [y/N]: ").strip().lower()
    if confirm == 'y':
        clear_tasks()
        print("✅ All tasks cleared.")
    else:
        print("Aborted.")

def handle_export(args):
    export_tasks(args.format, args.output)
    print(f"📤 Tasks exported to {args.output}")
    log_action(f"Exported tasks to {args.output}")

def handle_import(args):
    import_tasks(args.file, args.format)
    print(f"📥 Tasks imported from {args.file}")
    log_action(f"Imported tasks from {args.file}")

def run_cli():
    parser = argparse.ArgumentParser(prog="lisa", description="Local Intelligent Scheduling Assistant (LISA)")
    subparsers = parser.add_subparsers(title="commands")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", type=str, help="Task description")
    add_parser.add_argument("--module", type=str, default="general", choices=VALID_MODULES, help=f"Task module ({', '.join(VALID_MODULES)})")
    add_parser.add_argument("--due", type=str, help="Due date (YYYY-MM-DD)")
    add_parser.add_argument("--priority", type=str, choices=PRIORITY_LEVELS, help="Task priority")
    add_parser.add_argument("--force", action="store_true", help="Allow duplicate task")
    add_parser.set_defaults(func=handle_add)

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--module", type=str, choices=VALID_MODULES, help="Filter by module")
    list_parser.set_defaults(func=handle_list)

    remove_parser = subparsers.add_parser("remove", help="Remove a task by ID")
    remove_parser.add_argument("id", type=int, help="Task ID to remove")
    remove_parser.set_defaults(func=handle_remove)

    clear_parser = subparsers.add_parser("clear", help="Clear all tasks (with confirmation)")
    clear_parser.set_defaults(func=handle_clear)

    export_parser = subparsers.add_parser("export", help="Export tasks to file")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json")
    export_parser.add_argument("--output", default="data/tasks_export.json")
    export_parser.set_defaults(func=handle_export)

    import_parser = subparsers.add_parser("import", help="Import tasks from file")
    import_parser.add_argument("--file", required=True)
    import_parser.add_argument("--format", choices=["json", "csv"], default="json")
    import_parser.set_defaults(func=handle_import)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
