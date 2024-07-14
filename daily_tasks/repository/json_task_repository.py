"""
This module defines a concrete implementation of a task repository using JSON files.
"""
import os
import json
from typing import Dict, Any

from daily_tasks.repository import TaskRepository
from daily_tasks.models import Task, TaskFilter

MAX_TASKS_PER_FILE = 2000

class JSONTaskRepository(TaskRepository):
    """Concrete implementation of a task repository using JSON files."""

    def __init__(self, *args, **kwargs):
        """Initialize the JSONTaskRepository."""
        super().__init__(*args, **kwargs)

        if self.dt_settings.json_settings is None:
            raise ValueError("json_settings must be provided")
        elif self.dt_settings.json_settings.tasks_path is None:
            raise ValueError("json_settings.tasks_path must be provided")

        tasks_path = self.dt_settings.json_settings.tasks_path
        os.makedirs(os.path.dirname(tasks_path), exist_ok=True)
        if not os.path.exists(tasks_path):
            with open(tasks_path, 'w+', encoding='utf-8') as fh:
                fh.write('[]')
            print(f'Created new tasks file at {tasks_path}')
        else:
            print(f'Using existing tasks file at {tasks_path}')

        self.tasks_path = tasks_path
        self.tasks: dict[int, Task] = {}
        self.next_id = None
        self.load_tasks()

    def load_tasks(self):
        """Load all tasks"""
        print(f'Loading tasks from {self.tasks_path}')
        with open(self.tasks_path, 'r', encoding='utf-8') as fh:
            records = json.load(fh)
            for record in records:
                task = Task(**record)
                self.tasks[task.id] = task
            self.next_id = len(records) + 1

    def _save_tasks(self):
        """Save all tasks"""
        if len(self.tasks) == 0:
            with open(self.tasks_path, 'w', encoding='utf-8') as fh:
                fh.write('[]')
                return
        elif len(self.tasks) >= MAX_TASKS_PER_FILE:
            raise ValueError(f"Maximum number of tasks per file exceeded: {MAX_TASKS_PER_FILE}; Delete some tasks first.")

        with open(self.tasks_path, 'w', encoding='utf-8') as fh:
            json.dump([task.model_dump() for task in self.tasks.values()], fh, indent=4)
            self.next_id = len(self.tasks) + 1

    def create_task(self, task: Task) -> Task:
        """
        Create a new task.

        Args:
            task: The task object to create.

        Returns:
            The created task object.
        """
        task.id = self.next_id
        self.tasks[task.id] = task
        self._save_tasks()
        return task

    def read_task(self, task_id: int) -> Task:
        """
        Read a task by its ID.

        Args:
            task_id: The ID of the task to read.

        Returns:
            The task object.
        """
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")
        return task

    def update_task(self, task_id: int, data: Dict[str, Any]) -> Task:
        """
        Update a task with new data.

        Args:
            task_id: The task object to update.
            data: The new data to update the task with.

        Returns:
            None

        Raises:
            ValueError: If the task with the given ID is not found.
        """
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")
        task.__dict__.update(data)
        self.tasks[task_id] = task
        self._save_tasks()
        return task

    def delete_task(self, task_id: int):
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            None

        Raises:
            ValueError: If the task with the given ID is not found.
        """
        task = self.tasks.pop(task_id, None)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")
        self._save_tasks()

    def list_tasks(self) -> list[Task]:
        """
        List all tasks.

        Returns:
            A list of task objects.
        """
        return list(self.tasks.values())
    
    def filter_tasks(self, filter_text: TaskFilter) -> list[Task]:
        """
        Filter tasks by text.

        Args:
            filter_text: The text to filter tasks by.

        Returns:
            A list of task objects.
        """
        if filter_text == TaskFilter.ACTIVE:
            return [task for task in self.tasks.values() if not task.completed]
        elif filter_text == TaskFilter.COMPLETED:
            return [task for task in self.tasks.values() if task.completed]
        else:
            return list(self.tasks.values())
