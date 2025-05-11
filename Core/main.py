import os
import json
from datetime import datetime

data_file = os.path.join("data", "tasks.json")


def load_tasks():
    if not os.path.exists(data_file):
        return []
    with open(data_file, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    with open(data_file, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(text, module):
    tasks = load_tasks()
    task_id = tasks[-1]["id"] + 1 if tasks else 1
    task = {
        "id": task_id,
        "text": text,
        "created": datetime.now().isoformat(),
        "module": module,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"[+] Added task #{task_id}: '{text}' [module: {module}]")


def list_tasks(module_filter=None):
    tasks = load_tasks()
    if module_filter:
        tasks = [t for t in tasks if t["module"] == module_filter]
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        print(f"#{t['id']} [{t['module']}] - {t['text']} (Created: {t['created']})")


def remove_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == len(new_tasks):
        print(f"[!] Task #{task_id} not found.")
    else:
        save_tasks(new_tasks)
        print(f"[-] Removed task #{task_id}.")
