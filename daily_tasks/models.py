from enum import Enum
from typing import Optional
from pydantic import BaseModel


class JSONSettings(BaseModel):
    tasks_path: str

class Settings(BaseModel):
    json_settings: JSONSettings

class Preferences(BaseModel):
    ...

class TaskFilter(Enum):
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
