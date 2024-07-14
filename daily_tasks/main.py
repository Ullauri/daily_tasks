"""
This module contains the main function for the daily_tasks application.
"""
import argparse
import os

from daily_tasks.config import load_config
from daily_tasks.ui import UI
from daily_tasks.repository import TaskRepository
from daily_tasks.task_manager import TaskManager


def main():
    """
    Entry point of the daily_tasks application.
    """
    config_file_path = os.environ.get("DT_CONFIG_PATH")
    print("DT_CONFIG_PATH: ", config_file_path)
    settings, preferences = load_config(config_file_path)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repository",
        type=str,
        help="Specify the repository type to use; options are 'json' or 'sqlite'"
    )
    parser.add_argument("ui", type=str, help="Specify the UI type; options are 'gtk'")
    args = parser.parse_args()

    repository: str = args.repository
    repository_class: TaskRepository = None
    if repository == "json":
        from daily_tasks.repository.json_task_repository import JSONTaskRepository
        repository_class = JSONTaskRepository

    ui: str = args.ui
    ui_class: UI = None
    if ui == "gtk":
        from daily_tasks.ui.gtk_ui import GTKTaskOverview
        ui_class = GTKTaskOverview

    task_manager = TaskManager(settings, preferences, ui_class, repository_class)
    task_manager.run()


if __name__ == "__main__":
    main()
