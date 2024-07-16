import unittest
from unittest.mock import MagicMock

from tests import test_settings, test_preferences
from daily_tasks.models import Task
from daily_tasks.repository import TaskRepository
from daily_tasks.ui import UI
from daily_tasks.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.settings = test_settings
        self.preferences = test_preferences

        self.gui_class = MagicMock(spec=UI)
        self.repository_class = MagicMock(spec=TaskRepository)
        
        self.repository = MagicMock(spec=TaskRepository)
        self.repository_class.return_value = self.repository

        self.task_manager = TaskManager(
            settings=self.settings,
            preferences=self.preferences,
            gui_class=self.gui_class,
            repository_class=self.repository_class
        )

    def test_handle_view_task_by_id(self):
        task = Task(title="Test Task", description="This is a test task")
        self.repository.read_task.return_value = task
        result = self.task_manager.handle_view_task_by_id(1)
        self.assertEqual(result, task)
        self.repository.read_task.assert_called_once_with(1)

    def test_handle_filter_tasks(self):
        task1 = Task(title="Task 1", description="This is task 1")
        task2 = Task(title="Task 2", description="This is task 2")
        self.repository.filter_tasks.return_value = [task1, task2]
        result = self.task_manager.handle_filter_tasks("task")
        self.assertEqual(result, [task1, task2])
        self.repository.filter_tasks.assert_called_once_with("task")

    def test_handle_create_task(self):
        task = Task(title="Test Task", description="This is a test task")
        self.task_manager.handle_create_task(task)
        self.repository.create_task.assert_called_once_with(task)

    def test_handle_edit_task(self):
        task_id = 1
        data = {"title": "Updated Task"}
        self.task_manager.handle_edit_task(task_id, data)
        self.repository.update_task.assert_called_once_with(task_id, data)

    def test_handle_delete_task(self):
        task_id = 1
        self.task_manager.handle_delete_task(task_id)
        self.repository.delete_task.assert_called_once_with(task_id)

    def test_handle_complete_task(self):
        task_id = 1
        self.task_manager.handle_complete_task(task_id)
        self.repository.update_task.assert_called_once_with(task_id, {'completed': True})


if __name__ == "__main__":
    unittest.main()