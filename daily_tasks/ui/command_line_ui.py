"""
Command line interface for the Daily Tasks application.
"""
import json

from enum import Enum
from typing import Callable, List, Dict, Any

from daily_tasks.models import Task, TaskFilter
from daily_tasks.ui import UI


def command_handler_decorator(func):
    """
    Decorator function for command handlers.

    This decorator function wraps the command handler functions and adds exception handling.
    If an exception occurs during the execution of the command handler, an error message is printed.

    Args:
        func (Callable): The command handler function to be decorated.

    Returns:
        Callable: The decorated command handler function.
    """
    def wrapper(*args, **kwargs):
        print('\n')
        print('--------------------------------')
        resp = False
        try:
            resp = func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")     
        print('--------------------------------')
        print('\n')   
        return resp
    return wrapper


class Command(Enum):
    """
    Enum class for command line interface commands.
    """
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    COMPLETE = "complete"
    LIST = "list"
    FILTER = "filter"
    EXIT = "exit"


class CommandLineUI(UI):
    """
    Command line interface for the Daily Tasks application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.on_create_task_callback = None
        self.on_edit_task_callback = None
        self.on_delete_task_callback = None
        self.on_complete_task_callback = None
        self.on_filter_tasks_callback = None
        self.on_get_task_by_index_callback = None
        self.on_get_task_by_id_callback = None

        self.tasks: List[Task] = kwargs["init_tasks"]

    def register_callbacks(
        self,
        on_get_task_by_index_callback: Callable[[int], Task],
        on_get_task_by_id_callback: Callable[[int], Task],
        on_filter_tasks_callback: Callable[[str], List[Task]],
        on_create_task_callback: Callable[[Task], List[Task]],
        on_edit_task_callback: Callable[[int, Dict[str, Any]], List[Task]],
        on_delete_task_callback: Callable[[int], List[Task]],
        on_complete_task_callback: Callable[[int], List[Task]],
    ):
        """
        Register callback functions for handling user commands.
        """
        self.on_create_task_callback = on_create_task_callback
        self.on_edit_task_callback = on_edit_task_callback
        self.on_delete_task_callback = on_delete_task_callback
        self.on_complete_task_callback = on_complete_task_callback
        self.on_filter_tasks_callback = on_filter_tasks_callback
        self.on_get_task_by_index_callback = on_get_task_by_index_callback
        self.on_get_task_by_id_callback = on_get_task_by_id_callback

    def handle_command(self):
        """
        Handles user commands in the command line interface.

        Prompts the user for a command, executes the corresponding command handler,
        and returns False to indicate that the program should continue running.

        Returns:
            bool: False to indicate that the program should continue running.
        """
        print('\n')
        self.print_help()
        command = input("Enter a command: ")
        print('\n')

        command_handler = {
            Command.CREATE.value: self.create_task,
            Command.EDIT.value: self.edit_task,
            Command.DELETE.value: self.delete_task,
            Command.COMPLETE.value: self.complete_task,
            Command.LIST.value: self.list_tasks,
            Command.FILTER.value: self.filter_tasks,
            Command.EXIT.value: self.exit,
        }

        if command in command_handler:
            return command_handler[command]()

        print("Invalid command")
        return False

    def launch(self):
        print("\nWelcome to Daily Tasks!")

        while True:
            should_exit = self.handle_command()
            if should_exit:
                break

    def print_help(self):
        """
        Prints the available commands for the command line interface.
        """
        print("Available commands:")
        print(f"{Command.CREATE.value} - Create a new task")
        print(f"{Command.EDIT.value} - Edit a task")
        print(f"{Command.DELETE.value} - Delete a task")
        print(f"{Command.COMPLETE.value} - Mark a task as Completed")
        print(f"{Command.LIST.value} - List all tasks")
        print(f"{Command.FILTER.value} - List tasks via filter")
        print(f"{Command.EXIT.value} - Exit the program")

    def print_task(self, task: Task):
        """
        Prints the details of a given task.

        Args:
            task (Task): The task object to be printed.

        Returns:
            None
        """
        print(json.dumps(task.__dict__, indent=4))

    def _list_tasks(self):
        for task in self.tasks:
            self.print_task(task)

    def exit(self):
        """
        Exits the program.
        """
        print("Good bye!")
        return True

    @command_handler_decorator
    def create_task(self):
        """
        Creates a new task by prompting the user for task details.
        The task is then passed to the `on_create_task_callback` method for further processing.
        If an exception occurs during the creation of the task, an error message is printed.
        """
        print("Creating a new task")
        title = input("Enter the title: ")
        description = input("Enter the description: ")
        task = Task(title=title, description=description)
        self.tasks = self.on_create_task_callback(task)
        print("Task created")

    @command_handler_decorator
    def edit_task(self):
        """
        Edit a task by providing a new title and description.

        This method prompts the user to enter the task ID of the task they want to edit.
        The user is then prompted to enter any new task details they wish to edit.
        """
        print("Editing a task")
        task_id = int(input("Enter the task ID: "))
        original_task = self.on_get_task_by_id_callback(task_id)
        title = input("Enter the new title (leave blank to keep original):")
        description = input("Enter the new description (leave blank to keep original):")
        new_title = original_task.title if title == "" else title
        new_description = original_task.description if description == "" else description
        self.tasks = self.on_edit_task_callback(
            task_id,
            {"title": new_title, "description": new_description}
        )
        print("Task updated")

    @command_handler_decorator
    def delete_task(self):
        """
        Deletes a task from the task list.
        
        This method prompts the user to enter the ID of the task they want to delete.
        It then calls the `on_delete_task_callback` method to handle the deletion.
        """
        print("Deleting a task")
        task_id = int(input("Enter the task ID: "))
        self.tasks = self.on_delete_task_callback(task_id)
        print("Task deleted")

    @command_handler_decorator
    def complete_task(self):
        """
        Completes a task by marking it as completed.

        This method prompts the user to enter the task ID of the task they want to complete.
        It then calls the `on_complete_task_callback` method with the task ID as an argument.
        The `on_complete_task_callback` method should handle the logic of marking the task as completed.
        """
        print("Completing a task")
        self._list_tasks()
        task_id = int(input("Enter the task ID: "))
        self.tasks = self.on_complete_task_callback(task_id)
        print("Task completed")

    @command_handler_decorator
    def list_tasks(self):
        """
        Print all tasks in the command line interface.
        """
        print("Listing all tasks")
        self._list_tasks()
        print("All tasks listed")

    @command_handler_decorator
    def filter_tasks(self):
        """
        Filter tasks based on a specified filter type.
        """
        print("Filtering tasks")
        filter_types = [f.value for f in TaskFilter]
        filter_type = input(f"Enter the filter type ({filter_types}): ")
        tasks = self.on_filter_tasks_callback(filter_type)
        if len(tasks) > 0:
            for task in tasks:
                self.print_task(task)
            print("Tasks filtered")
        else:
            print("No tasks found")
