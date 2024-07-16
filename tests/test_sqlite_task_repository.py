import unittest
import os
import tempfile

from tests import test_settings, test_preferences
from daily_tasks.models import Task, TaskFilter
from daily_tasks.repository.sqlite_task_repository import SQLiteTaskRepository


class TestSQLiteTaskRepository(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Update the settings to use the temporary database path
        self.settings = test_settings
        self.settings.sqlite_settings.db_path = self.db_path
        self.preferences = test_preferences
        self.repository = SQLiteTaskRepository(dt_settings=self.settings, dt_preferences=self.preferences)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_create_task(self):
        task = Task(title="Test Task", description="This is a test task", completed=False)
        created_task = self.repository.create_task(task)
        self.assertIsNotNone(created_task.id)
        self.assertEqual(created_task.title, "Test Task")
        self.assertEqual(created_task.description, "This is a test task")
        self.assertFalse(created_task.completed)

    def test_read_task(self):
        task = Task(title="Test Task", description="This is a test task", completed=False)
        created_task = self.repository.create_task(task)
        read_task = self.repository.read_task(created_task.id)
        self.assertEqual(read_task.id, created_task.id)
        self.assertEqual(read_task.title, created_task.title)
        self.assertEqual(read_task.description, created_task.description)
        self.assertEqual(read_task.completed, created_task.completed)

    def test_update_task(self):
        task = Task(title="Test Task", description="This is a test task", completed=False)
        created_task = self.repository.create_task(task)
        updated_task = self.repository.update_task(created_task.id, {"title": "Updated Task", "completed": True})
        self.assertEqual(updated_task.id, created_task.id)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertTrue(updated_task.completed)

    def test_delete_task(self):
        task = Task(title="Test Task", description="This is a test task", completed=False)
        created_task = self.repository.create_task(task)
        self.repository.delete_task(created_task.id)
        with self.assertRaises(ValueError):
            self.repository.read_task(created_task.id)

    def test_list_tasks(self):
        task1 = Task(title="Task 1", description="First task", completed=False)
        task2 = Task(title="Task 2", description="Second task", completed=True)
        self.repository.create_task(task1)
        self.repository.create_task(task2)
        tasks = self.repository.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].title, "Task 2")

    def test_filter_tasks_all(self):
        task1 = Task(title="Task 1", description="First task", completed=False)
        task2 = Task(title="Task 2", description="Second task", completed=True)
        self.repository.create_task(task1)
        self.repository.create_task(task2)
        tasks = self.repository.filter_tasks(TaskFilter.ALL.value)
        self.assertEqual(len(tasks), 2)

    def test_filter_tasks_completed(self):
        task1 = Task(title="Task 1", description="First task", completed=False)
        task2 = Task(title="Task 2", description="Second task", completed=True)
        self.repository.create_task(task1)
        self.repository.create_task(task2)
        tasks = self.repository.filter_tasks(TaskFilter.COMPLETED.value)
        self.assertEqual(len(tasks), 1)
        self.assertTrue(tasks[0].completed)

    def test_filter_tasks_active(self):
        task1 = Task(title="Task 1", description="First task", completed=False)
        task2 = Task(title="Task 2", description="Second task", completed=True)
        self.repository.create_task(task1)
        self.repository.create_task(task2)
        tasks = self.repository.filter_tasks(TaskFilter.ACTIVE.value)
        self.assertEqual(len(tasks), 1)
        self.assertFalse(tasks[0].completed)

    def test_full_user_flow(self):
        # Step 1: Create 2 tasks
        task1 = Task(title="Task 1", description="First task", completed=False)
        task2 = Task(title="Task 2", description="Second task", completed=False)
        created_task1 = self.repository.create_task(task1)
        created_task2 = self.repository.create_task(task2)

        # Step 2: View task
        read_task1 = self.repository.read_task(created_task1.id)
        self.assertEqual(read_task1.id, created_task1.id)
        self.assertEqual(read_task1.title, created_task1.title)
        self.assertEqual(read_task1.description, created_task1.description)
        self.assertEqual(read_task1.completed, created_task1.completed)

        # Step 3: Edit one task
        updated_task1 = self.repository.update_task(created_task1.id, {"title": "Updated Task 1"})
        self.assertEqual(updated_task1.id, created_task1.id)
        self.assertEqual(updated_task1.title, "Updated Task 1")

        # Step 4: Complete one task
        completed_task2 = self.repository.update_task(created_task2.id, {"completed": True})
        self.assertEqual(completed_task2.id, created_task2.id)
        self.assertTrue(completed_task2.completed)

        # Step 5: List tasks
        tasks = self.repository.list_tasks()
        self.assertEqual(len(tasks), 2)

        # Step 6: Filter tasks for active
        active_tasks = self.repository.filter_tasks(TaskFilter.ACTIVE.value)
        self.assertEqual(len(active_tasks), 1)
        self.assertFalse(active_tasks[0].completed)

        # Step 7: Filter tasks for completed
        completed_tasks = self.repository.filter_tasks(TaskFilter.COMPLETED.value)
        self.assertEqual(len(completed_tasks), 1)
        self.assertTrue(completed_tasks[0].completed)

        # Step 8: Delete task
        self.repository.delete_task(created_task1.id)

        # Step 9: List tasks
        tasks_after_deletion = self.repository.list_tasks()
        self.assertEqual(len(tasks_after_deletion), 1)
        self.assertEqual(tasks_after_deletion[0].id, created_task2.id)

        # Step 10: View task (expecting a ValueError because the task was deleted)
        with self.assertRaises(ValueError):
            self.repository.read_task(created_task1.id)

if __name__ == "__main__":
    unittest.main()
