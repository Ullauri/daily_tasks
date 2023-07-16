"""
This module defines an abstract base class for a task repository.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from daily_tasks.models import Task, Settings, Preferences


class TaskRepository(ABC):
    """Abstract base class for a task repository."""

    def __init__(self, *args, dt_settings: Settings = None, dt_preferences: Preferences = None, **kwargs):
        if dt_settings is None:
            raise ValueError("dt_settings must be provided")

        if dt_preferences is None:
            raise ValueError("dt_preferences must be provided")

        self.dt_settings = dt_settings
        self.dt_preferences = dt_preferences

    @abstractmethod
    def create_task(self, task: Task) -> Task:
        """Create a new task.

        Args:
            task: The task object to create.

        Returns:
            None
        """

    @abstractmethod
    def read_task(self, task_id: int) -> Task:
        """Read a task by its ID.

        Args:
            task_id: The ID of the task to read.

        Returns:
            The task object.
        """

    @abstractmethod
    def update_task(self, task_id: int, data: Dict[str, Any]) -> Task:
        """Update a task with new data.

        Args:
            task_id: The task object to update.
            data: The new data to update the task with.

        Returns:
            None
        """

    @abstractmethod
    def delete_task(self, task_id: int):
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            None
        """

    @abstractmethod
    def list_tasks(self) -> list[Task]:
        """List all tasks.

        Returns:
            A list of task objects.
        """

    @abstractmethod
    def filter_tasks(self, filter_text: str) -> list[Task]:
        """Filter tasks by text.

        Args:
            filter_text: The text to filter tasks by.

        Returns:
            A list of task objects.
        """
