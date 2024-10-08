from enum import Enum
from typing import Optional
from pydantic import BaseModel


class JSONSettings(BaseModel):
    tasks_path: str


class SQLiteSettings(BaseModel):
    db_path: str


class Settings(BaseModel):
    json_settings: JSONSettings
    sqlite_settings: SQLiteSettings


class GTKUIPreferences(BaseModel):
    default_window_width: int
    default_window_height: int
    max_window_width: int
    max_window_height: int


class Preferences(BaseModel):
    gtk_ui: GTKUIPreferences


class TaskFilter(Enum):
    """
    Enum class for task filters.
    """
    ALL = "all"
    COMPLETED = "completed"
    ACTIVE = "active"


class Task(BaseModel):
    """
    Task.

    Attributes:
        id (int): The unique identifier of the task.
        title (str): The title of the task.
        description (str): The description of the task.
        completed (bool): Whether the task is completed or not.
    """
    id: Optional[int] = None
    title: str
    description: str
    completed: bool = False

    def description_display_text(self, limit=50) -> str:
        """
        Get the display text for the description.

        Returns:
            The display text for the description.
        """
        return self.description[:limit] + '...'
