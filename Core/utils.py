import json
import logging
from pathlib import Path

TASKS_FILE = Path(__file__).parent.parent / 'data' / 'tasks.json'
LOG_FILE = Path(__file__).parent.parent / 'logs' / 'lisa.log'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def load_tasks():
    try:
        if not TASKS_FILE.exists():
            return []
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"Failed to load tasks: {e}")
        return []

def save_tasks(tasks):
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
        logging.info("Tasks saved successfully.")
    except IOError as e:
        logging.error(f"Failed to save tasks: {e}")

def get_next_id(tasks):
    return max((task['id'] for task in tasks), default=0) + 1
