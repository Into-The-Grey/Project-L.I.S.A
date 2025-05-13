import json
import csv
import logging
from pathlib import Path

TASKS_FILE = Path(__file__).parent.parent / 'data' / 'tasks.json'
LOG_FILE = Path(__file__).parent.parent / 'logs' / 'lisa.log'

VALID_MODULES = ["work", "home", "study"]
PRIORITY_LEVELS = ["low", "medium", "high"]

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def log_action(message):
    logging.info(message)

def load_tasks():
    try:
        if not TASKS_FILE.exists():
            return []
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        log_action(f"ERROR loading tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
        log_action("Saved task list.")
    except IOError as e:
        log_action(f"ERROR saving tasks: {e}")

def get_next_id(tasks):
    return max((task['id'] for task in tasks), default=0) + 1

def clear_tasks():
    save_tasks([])

def export_tasks(fmt, output_file):
    tasks = load_tasks()
    path = Path(output_file)
    if not tasks:
        return
    if fmt == "json":
        with open(path, "w") as f:
            json.dump(tasks, f, indent=2)
    elif fmt == "csv":
        with open(path, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
            writer.writeheader()
            writer.writerows(tasks)

def import_tasks(file, fmt):
    path = Path(file)
    if not path.exists():
        log_action(f"Import file not found: {file}")
        return
    if fmt == "json":
        with open(path, "r") as f:
            new_tasks = json.load(f)
    elif fmt == "csv":
        with open(path, "r", newline='') as f:
            reader = csv.DictReader(f)
            new_tasks = list(reader)

    existing = load_tasks()
    new_ids = {int(t['id']) for t in existing}
    for t in new_tasks:
        t['id'] = int(t['id'])
        if t['id'] not in new_ids:
            existing.append(t)
    save_tasks(existing)
