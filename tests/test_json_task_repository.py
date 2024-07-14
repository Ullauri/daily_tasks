import os
import unittest

from tests import test_settings, test_preferences
from daily_tasks.models import Task, TaskFilter
from daily_tasks.repository.json_task_repository import JSONTaskRepository


class TestJSONTaskRepository(unittest.TestCase):
    def setUp(self):
        self.repository = JSONTaskRepository(dt_settings=test_settings, dt_preferences=test_preferences)

    def tearDown(self):
        os.remove(self.repository.tasks_path)

    def test_create_task(self):
        task = Task(title="Test Task", description="This is a test task")
        created_task = self.repository.create_task(task)
        self.assertEqual(created_task.title, "Test Task")
        self.assertEqual(created_task.description, "This is a test task")

    def test_read_task(self):
        task = Task(title="Test Task", description="This is a test task")
        created_task = self.repository.create_task(task)
        retrieved_task = self.repository.read_task(created_task.id)
        self.assertEqual(retrieved_task.title, "Test Task")
        self.assertEqual(retrieved_task.description, "This is a test task")

    def test_update_task(self):
        task = Task(title="Test Task", description="This is a test task")
        created_task = self.repository.create_task(task)
        updated_task = self.repository.update_task(created_task.id, {"title": "Updated Task"})
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "This is a test task")

    def test_delete_task(self):
        task = Task(title="Test Task", description="This is a test task")
        created_task = self.repository.create_task(task)
        self.repository.delete_task(created_task.id)
        with self.assertRaises(ValueError):
            self.repository.read_task(created_task.id)

    def test_list_tasks(self):
        task1 = Task(title="Task 1", description="This is task 1")
        task2 = Task(title="Task 2", description="This is task 2")
        self.repository.create_task(task1)
        self.repository.create_task(task2)
        tasks = self.repository.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")

    def test_filter_tasks(self):
        task1 = Task(title="Task 1", description="This is task 1", completed=False)
        task2 = Task(title="Task 2", description="This is task 2", completed=True)
        self.repository.create_task(task1)
        self.repository.create_task(task2)
        active_tasks = self.repository.filter_tasks(TaskFilter.ACTIVE)
        completed_tasks = self.repository.filter_tasks(TaskFilter.COMPLETED)
        all_tasks = self.repository.filter_tasks(TaskFilter.ALL)
        self.assertEqual(len(active_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(len(all_tasks), 2)
        self.assertEqual(active_tasks[0].title, "Task 1")
        self.assertEqual(completed_tasks[0].title, "Task 2")
        self.assertEqual(all_tasks[0].title, "Task 1")
        self.assertEqual(all_tasks[1].title, "Task 2")

if __name__ == "__main__":
    unittest.main()
