"""
This module defines an abstract base class for a UI manager.
"""
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Any

from daily_tasks.models import Settings, Preferences, Task, TaskFilter


class UI(ABC):
    """
    Abstract base class for a Task Manager UI.
    """
    description_limit = 50

    def __init__(
            self,
            *args,
            dt_settings: Settings=None,
            dt_preferences: Preferences=None,
            init_tasks: List[Task]=None,
            **kwargs
        ):
        """
        Initialize the UI manager.
        """
        super().__init__(*args, **kwargs)
        if dt_settings is None:
            raise ValueError("dt_settings must be provided")
        if dt_preferences is None:
            raise ValueError("dt_preferences must be provided")
        if init_tasks is None:
            raise ValueError("init_tasks must be provided")

        self.dt_settings = dt_settings
        self.dt_preferences = dt_preferences

    @abstractmethod
    def register_callbacks(
        self,
        on_get_task_by_index_callback: Callable[[int], Task],
        on_get_task_by_id_callback: Callable[[int], Task],
        on_filter_tasks_callback: Callable[[TaskFilter], List[Task]],
        on_create_task_callback: Callable[[Task], List[Task]],
        on_edit_task_callback: Callable[[int, Dict[str, Any]], List[Task]],
        on_delete_task_callback: Callable[[int], List[Task]],
        on_complete_task_callback: Callable[[int], List[Task]],
    ):
        """
        Register the callbacks for the UI.

        Relates to from daily_tasks.repository import TaskRepository

        Args:
            on_get_task_by_index_callback: The callback to view a task by index.
            on_get_task_by_id_callback: The callback to view a task by id.
            on_filter_tasks_callback: The callback to filter tasks.
            on_create_task_callback: The callback to create a task.
            on_edit_task_callback: The callback to edit a task.
            on_delete_task_callback: The callback to delete a task.
            on_complete_task_callback: The callback to complete a task.
        
        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented.
        """

    @abstractmethod
    def launch(self):
        """
        Launch the UI.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
