import argparse
import argcomplete
import os
from datetime import datetime, timedelta
from .utils import (
    load_tasks,
    save_tasks,
    get_next_id,
    log_action,
    VALID_MODULES,
    PRIORITY_LEVELS,
    export_tasks,
    import_tasks,
    clear_tasks,
)

# --- prompt_toolkit imports for menu ---
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog, yes_no_dialog

# --- dotenv import and load ---
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
# -----------------------------


def handle_add(args):
    tasks = load_tasks()
    text = args.text.strip()
    if not text:
        print("Error: Task description cannot be empty.")
        return

    if args.module not in VALID_MODULES:
        print(f"Error: Invalid module. Choose from: {', '.join(VALID_MODULES)}")
        return

    if (
        any(t["text"] == text and t["module"] == args.module for t in tasks)
        and not args.force
    ):
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
        "priority": args.priority or "medium",
    }
    tasks.append(new_task)
    save_tasks(tasks)
    log_action(f"Added task {new_task['id']}: {text} [{args.module}]")
    print(f"✅ Task added: [{new_task['id']}] {text}")


def handle_list(args):
    tasks = load_tasks()
    if args.module:
        tasks = [t for t in tasks if t["module"] == args.module]
    tasks.sort(key=lambda x: (x.get("due") or "", x["id"]))
    for task in tasks:
        print(
            f"[{task['id']}] ({task['module']}) {task['text']} | Due: {task.get('due', '-')} | Priority: {task.get('priority', '-')}"
        )
    log_action("Listed tasks")


def handle_remove(args):
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != args.id]
    if len(tasks) == before:
        print(f"⚠️ Task ID {args.id} not found.")
    else:
        print(f"🗑️ Task {args.id} removed.")
        log_action(f"Removed task {args.id}")
    save_tasks(tasks)


def handle_clear(args):
    confirm = (
        input("Are you sure you want to delete all tasks? [y/N]: ").strip().lower()
    )
    if confirm == "y":
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


def handle_check_reminders(args):
    from datetime import datetime, timedelta
    import dateparser
    from .utils import load_tasks, save_tasks, log_action
    from dotenv import load_dotenv
    import os

    load_dotenv(dotenv_path=".env")

    # Parse time window
    now = datetime.now()
    since = now - timedelta(hours=1)
    until = now

    # Interval comes from CLI > ENV > default
    interval_seconds = int(args.interval) if args.interval else \
                       int(os.getenv("LISA_REMIND_INTERVAL", "3600"))

    if hasattr(args, "since") and args.since:
        since_parsed = dateparser.parse(args.since)
        if since_parsed:
            since = since_parsed

    if hasattr(args, "until") and args.until:
        until_parsed = dateparser.parse(args.until)
        if until_parsed:
            until = until_parsed

    tasks = load_tasks()
    reminders_triggered = 0

    for task in tasks:
        due_str = task.get("due")
        if not due_str:
            continue

        due_dt = dateparser.parse(due_str)
        if not due_dt:
            log_action(
                f"REMINDER_PARSE_ERROR: Task {task.get('id')} has unparseable due date: {due_str}"
            )
            continue

        if not (since <= due_dt <= until):
            log_action(
                f"REMINDER_SKIPPED: Task {task.get('id')} not in time window ({since} → {until})"
            )
            continue

        if task.get("acknowledged"):
            log_action(f"REMINDER_SKIPPED: Task {task['id']} acknowledged")
            continue

        if not getattr(args, "all", False):
            last_reminded = task.get("last_reminded")
            if last_reminded:
                try:
                    last_dt = datetime.fromisoformat(last_reminded)
                    if (now - last_dt).total_seconds() < interval_seconds:
                        log_action(
                            f"REMINDER_SKIPPED: Task {task['id']} reminded recently ({last_reminded})"
                        )
                        continue
                except ValueError:
                    log_action(
                        f"REMINDER_PARSE_ERROR: Invalid last_reminded for task {task['id']}"
                    )

        print(
            f"🔔 [{task['id']}] {task['text']} (due: {due_dt.date()}) [{task['module']}]"
        )
        log_action(f"REMINDER_TRIGGER: Task {task['id']} is due → {task['text']}")

        if not getattr(args, "dry_run", False):
            task["last_reminded"] = now.isoformat()

        reminders_triggered += 1

    if not getattr(args, "dry_run", False):
        save_tasks(tasks)

    if reminders_triggered == 0:
        print("⏰ No reminders to trigger.")
        log_action("REMINDER_CHECK: no matches in window.")


# --- Interactive menu function ---
def menu_loop():
    while True:
        print("\n== LISA Assistant Menu ==")
        options = [
            "List Tasks",
            "Add Task",
            "Remove Task",
            "Export Tasks",
            "Import Tasks",
            "Clear All Tasks",
            "Exit",
        ]
        action_completer = WordCompleter(options, ignore_case=True)
        choice = prompt("Choose action: ", completer=action_completer).strip().lower()

        if choice.startswith("list"):
            tasks = load_tasks()
            for t in tasks:
                print(
                    f"[{t['id']}] ({t['module']}) {t['text']} | Due: {t.get('due', '-')} | Priority: {t.get('priority', '-')}"
                )
        elif choice.startswith("add"):
            text = prompt("Task description: ").strip()
            module = radiolist_dialog(
                title="Choose Module",
                text="Select task context:",
                values=[(m, m) for m in VALID_MODULES],
            ).run()
            due = prompt("Due date (YYYY-MM-DD) [optional]: ").strip()
            priority = radiolist_dialog(
                title="Set Priority",
                text="Select priority:",
                values=[(p, p) for p in PRIORITY_LEVELS],
            ).run()
            if not text or not module or not priority:
                print("⚠️ Task not added (missing input).")
                continue
            task = {
                "id": get_next_id(load_tasks()),
                "text": text,
                "created": datetime.now().isoformat(),
                "module": module,
                "due": due if due else None,
                "priority": priority,
            }
            tasks = load_tasks()
            tasks.append(task)
            save_tasks(tasks)
            log_action(f"Menu-add: {task['id']} {text}")
            print(f"✅ Task added: {text}")
        elif choice.startswith("remove"):
            task_id = prompt("Task ID to remove: ").strip()
            if task_id.isdigit():
                task_id = int(task_id)
                tasks = [t for t in load_tasks() if t["id"] != task_id]
                save_tasks(tasks)
                print(f"🗑️ Task {task_id} removed.")
                log_action(f"Menu-remove: {task_id}")
            else:
                print("Invalid ID.")
        elif choice.startswith("export"):
            fmt = radiolist_dialog(
                title="Export Format",
                text="Choose export format:",
                values=[("json", "JSON"), ("csv", "CSV")],
            ).run()
            out_path = prompt(
                "Export to file (default: data/tasks_export.json): "
            ).strip()
            if not out_path:
                out_path = (
                    "data/tasks_export.json"
                    if fmt == "json"
                    else "data/tasks_export.csv"
                )
            export_tasks(fmt, out_path)
            print(f"📤 Tasks exported to {out_path}")
        elif choice.startswith("import"):
            fmt = radiolist_dialog(
                title="Import Format",
                text="Choose import format:",
                values=[("json", "JSON"), ("csv", "CSV")],
            ).run()
            path = prompt("Import from file: ").strip()
            import_tasks(path, fmt)
            print(f"📥 Imported tasks from {path}")
        elif choice.startswith("clear"):
            if yes_no_dialog(title="Confirm", text="Clear ALL tasks?").run():
                clear_tasks()
                print("✅ All tasks cleared.")
                log_action("Menu-clear")
        elif choice.startswith("exit"):
            print("Goodbye.")
            break
        else:
            print("Unrecognized command.")


# ---------------------------------


def handle_menu(args):
    menu_loop()


def run_cli():
    parser = argparse.ArgumentParser(
        prog="lisa", description="Local Intelligent Scheduling Assistant (LISA)"
    )
    subparsers = parser.add_subparsers(title="commands")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", type=str, help="Task description")
    add_parser.add_argument(
        "--module",
        type=str,
        default="general",
        choices=VALID_MODULES,
        help=f"Task module ({', '.join(VALID_MODULES)})",
    )
    add_parser.add_argument("--due", type=str, help="Due date (YYYY-MM-DD)")
    add_parser.add_argument(
        "--priority", type=str, choices=PRIORITY_LEVELS, help="Task priority"
    )
    add_parser.add_argument("--force", action="store_true", help="Allow duplicate task")
    add_parser.set_defaults(func=handle_add)

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--module", type=str, choices=VALID_MODULES, help="Filter by module"
    )
    list_parser.set_defaults(func=handle_list)

    remove_parser = subparsers.add_parser("remove", help="Remove a task by ID")
    remove_parser.add_argument("id", type=int, help="Task ID to remove")
    remove_parser.set_defaults(func=handle_remove)

    clear_parser = subparsers.add_parser(
        "clear", help="Clear all tasks (with confirmation)"
    )
    clear_parser.set_defaults(func=handle_clear)

    export_parser = subparsers.add_parser("export", help="Export tasks to file")
    export_parser.add_argument("--format", choices=["json", "csv"], default="json")
    export_parser.add_argument("--output", default="data/tasks_export.json")
    export_parser.set_defaults(func=handle_export)

    import_parser = subparsers.add_parser("import", help="Import tasks from file")
    import_parser.add_argument(
        "--file", required=True, help="Path to the file to import (required)"
    )
    import_parser.add_argument("--format", choices=["json", "csv"], default="json")
    import_parser.set_defaults(func=handle_import)

    # --- Add menu subcommand ---
    menu_parser = subparsers.add_parser("menu", help="Interactive menu mode")
    menu_parser.set_defaults(func=handle_menu)
    # ---------------------------

    # --- Add check-reminders subcommand ---
    check_parser = subparsers.add_parser("check-reminders", help="Scan for due tasks")
    check_parser.add_argument(
        "--since", type=str, help="Start of due window (e.g. '2024-06-01 09:00')"
    )
    check_parser.add_argument(
        "--until", type=str, help="End of due window (e.g. '2024-06-01 18:00')"
    )
    check_parser.add_argument(
        "--interval", type=int, help="Minimum seconds between reminders (default: 3600)"
    )
    check_parser.add_argument(
        "--all", action="store_true", help="Ignore last reminded time"
    )
    check_parser.add_argument(
        "--dry-run", action="store_true", help="Don't update last_reminded or save"
    )
    check_parser.set_defaults(func=handle_check_reminders)
    # --------------------------------------

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
