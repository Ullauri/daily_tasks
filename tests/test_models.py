import unittest
from daily_tasks.models import Task


class TestTask(unittest.TestCase):
    def test_description_display_text(self):
        task = Task(title="Test Task", description="This is a test task description", completed=False)
        expected_display_text = "This is a test task description..."
        self.assertEqual(task.description_display_text(), expected_display_text)


if __name__ == "__main__":
    unittest.main()