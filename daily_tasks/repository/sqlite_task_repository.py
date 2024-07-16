"""
SQLite task repository implementation.
"""
import sqlite3
from typing import Dict, Any, List
from daily_tasks.models import Task, Settings, Preferences, TaskFilter
from daily_tasks.repository import TaskRepository


class SQLiteTaskRepository(TaskRepository):
    """SQLite task repository implementation."""
    def __init__(self, dt_settings: Settings, dt_preferences: Preferences):
        super().__init__(dt_settings=dt_settings, dt_preferences=dt_preferences)
        self.db_path = dt_settings.sqlite_settings.db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database and create the tasks table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    completed BOOLEAN NOT NULL
                )
            ''')
            conn.commit()

    def create_task(self, task: Task) -> Task:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, completed)
                VALUES (?, ?, ?)
            ''', (task.title, task.description, task.completed))
            task.id = cursor.lastrowid
            conn.commit()
        return task

    def read_task(self, task_id: int) -> Task:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, title, description, completed FROM tasks WHERE id = ?',
                (task_id,)
            )
            row = cursor.fetchone()
            if row:
                return Task(id=row[0], title=row[1], description=row[2], completed=row[3])
            else:
                raise ValueError(f"Task with id {task_id} does not exist")

    def update_task(self, task_id: int, data: Dict[str, Any]) -> Task:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            columns = []
            values = []
            for key, value in data.items():
                columns.append(f"{key} = ?")
                values.append(value)
            values.append(task_id)
            cursor.execute(f'''
                UPDATE tasks
                SET {', '.join(columns)}
                WHERE id = ?
            ''', values)
            conn.commit()
        return self.read_task(task_id)

    def delete_task(self, task_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()

    def list_tasks(self) -> List[Task]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, description, completed FROM tasks')
            rows = cursor.fetchall()
        return [Task(id=row[0], title=row[1], description=row[2], completed=row[3]) for row in rows]

    def filter_tasks(self, filter_text: TaskFilter) -> List[Task]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if filter_text == TaskFilter.ALL.value:
                cursor.execute(
                    'SELECT id, title, description, completed FROM tasks'
                )
            elif filter_text == TaskFilter.COMPLETED.value:
                cursor.execute(
                    'SELECT id, title, description, completed FROM tasks WHERE completed = 1'
                )
            elif filter_text == TaskFilter.ACTIVE.value:
                cursor.execute(
                    'SELECT id, title, description, completed FROM tasks WHERE completed = 0'
                )
            rows = cursor.fetchall()
        return [Task(id=row[0], title=row[1], description=row[2], completed=row[3]) for row in rows]
