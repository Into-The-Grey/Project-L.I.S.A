import unittest
from ..Core import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.sample_tasks = [
            {
                "id": 1,
                "text": "Test task",
                "created": "2025-01-01T12:00:00",
                "module": "test",
            }
        ]
        utils.save_tasks(self.sample_tasks)

    def test_load_tasks(self):
        tasks = utils.load_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["text"], "Test task")

    def test_get_next_id(self):
        next_id = utils.get_next_id(self.sample_tasks)
        self.assertEqual(next_id, 2)

    def test_save_and_load_cycle(self):
        utils.save_tasks(self.sample_tasks)
        loaded = utils.load_tasks()
        self.assertEqual(loaded, self.sample_tasks)


if __name__ == "__main__":
    unittest.main()
