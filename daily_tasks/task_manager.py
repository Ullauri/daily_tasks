"""
This module contains the TaskManager class, which is responsible for orchestrating both
gui and repository classes to provide a complete task management system.
"""
from typing import List, Dict, Any
from daily_tasks.models import Task, Settings, Preferences
from daily_tasks.task_repository import TaskRepository
from daily_tasks.ui import UI


class TaskManager:
    """
    Application Orchestrator.
    """
    def __init__(self, settings: Settings, preferences: Preferences, gui_class: UI, repository_class: TaskRepository):
        """
        Initializes a new instance of the TaskManager class.

        Args:
            tasks_file_path (str): The path to the JSON file that stores the tasks.

        Raises:
            ValueError: If tasks_file_path is None.
        """
        if settings is None:
            raise ValueError("settings must be provided")
        self.settings = settings

        if preferences is None:
            raise ValueError("preferences must be provided")
        self.preferences = preferences

        if gui_class is None:
            raise ValueError("gui_class must be provided")
        self.ui_class = gui_class

        if repository_class is None:
            raise ValueError("repository_class must be provided")
        self.repository_class = repository_class
        self.repository: TaskRepository = self.repository_class(dt_settings=settings, dt_preferences=preferences)


        self.visible_tasks: List[Task] = self.repository.list_tasks()
        self.gui: UI = self.ui_class(
            dt_settings=settings,
            dt_preferences=preferences,
            init_tasks=self.visible_tasks,
        )

    def run(self):
        """
        Run the task manager application.
        """
        print("Running task manager application...")
        self.gui.register_callbacks(
            self.handle_view_task_by_index,
            self.handle_view_task_by_id,
            self.handle_filter_tasks,
            self.handle_create_task,
            self.handle_edit_task,
            self.handle_delete_task,
            self.handle_complete_task,
        )
        self.gui.launch()
    
    def handle_view_task_by_index(self, task_index: int) -> Task:
        """
        Handle the view task event.

        Args:
            task_index: The index of the task to view.
        """
        return self.visible_tasks[task_index]

    def handle_view_task_by_id(self, task_id: int) -> Task:
        """
        Handle the view task event.

        Args:
            task_id: The ID of the task to view.
        """
        return self.repository.read_task(task_id)

    def handle_filter_tasks(self, filter_text: str) -> List[Task]:
        """
        Handle the filter tasks event.

        Args:
            filter_text: The text to filter tasks by.
        """
        self.visible_tasks = self.repository.filter_tasks(filter_text)
        return self.visible_tasks

    def handle_create_task(self, task: Task) -> List[Task]:
        """
        Handle the create task event.

        Args:
            task: The task to create.
        """
        self.repository.create_task(task)
        self.visible_tasks = self.repository.list_tasks()
        return self.visible_tasks

    def handle_edit_task(self, task_id: int, data: Dict[str, Any]) -> List[Task]:
        """
        Handle the edit task event.

        Args:
            task_id: The ID of the task to edit.
            task: The updated task.
        """
        self.repository.update_task(task_id, data)
        self.visible_tasks = self.repository.list_tasks()
        return self.visible_tasks

    def handle_delete_task(self, task_id: int) -> List[Task]:
        """
        Handle the delete task event.

        Args:
            task_id: The ID of the task to delete.
        """
        self.repository.delete_task(task_id)
        self.visible_tasks = self.repository.list_tasks()
        return self.visible_tasks

    def handle_complete_task(self, task_id: int) -> List[Task]:
        """
        Handle the complete task event.

        Args:
            task_id: The ID of the task to complete.
        """
        self.repository.update_task(task_id, {'completed': True})
        self.visible_tasks = self.repository.list_tasks()
        return self.visible_tasks
