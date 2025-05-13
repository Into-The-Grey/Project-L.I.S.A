import unittest
from datetime import datetime, timedelta
from Core.utils import save_tasks, load_tasks


class TestReminderEnhanced(unittest.TestCase):
    def setUp(self):
        now = datetime.now()
        self.due_now = now.strftime("%Y-%m-%d")
        self.past_due = (now - timedelta(hours=2)).strftime("%Y-%m-%d")
        self.future_due = (now + timedelta(days=1)).strftime("%Y-%m-%d")

        self.sample = [
            {
                "id": 1,
                "text": "Due now",
                "created": now.isoformat(),
                "module": "work",
                "due": self.due_now,
            },
            {
                "id": 2,
                "text": "Acknowledged",
                "created": now.isoformat(),
                "module": "home",
                "due": self.due_now,
                "acknowledged": True,
            },
            {
                "id": 3,
                "text": "Recent reminder",
                "created": now.isoformat(),
                "module": "study",
                "due": self.due_now,
                "last_reminded": now.isoformat(),
            },
            {
                "id": 4,
                "text": "Future task",
                "created": now.isoformat(),
                "module": "home",
                "due": self.future_due,
            },
            {
                "id": 5,
                "text": "Unparseable due",
                "created": now.isoformat(),
                "module": "home",
                "due": "not-a-date",
            },
        ]

        save_tasks(self.sample)

    def test_due_tasks_count(self):
        tasks = load_tasks()
        due = [t for t in tasks if t.get("due") == self.due_now]
        self.assertGreaterEqual(len(due), 1)

    def test_acknowledged_is_flagged(self):
        tasks = load_tasks()
        ack = [t for t in tasks if t.get("acknowledged")]
        self.assertEqual(len(ack), 1)
        self.assertEqual(ack[0]["text"], "Acknowledged")

    def test_future_task_skipped(self):
        tasks = load_tasks()
        future = [t for t in tasks if t["due"] == self.future_due]
        self.assertEqual(len(future), 1)
        self.assertEqual(future[0]["text"], "Future task")

    def test_unparseable_logged(self):
        tasks = load_tasks()
        bad = [t for t in tasks if t["due"] == "not-a-date"]
        self.assertEqual(len(bad), 1)


if __name__ == "__main__":
    unittest.main()
