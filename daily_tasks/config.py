"""
This module provides functions for loading and managing configuration settings and preferences.
"""
import os
import json

from typing import Dict

from daily_tasks.models import Settings, Preferences


def load_config(config_path:str=None) -> tuple[Settings, Preferences]:
    """
    Load the configuration settings and preferences from the specified config path.

    Args:
        config_path (str, optional): The path to the configuration directory. If not provided,
            the default path will be used.

    Returns:
        tuple: A tuple containing the loaded settings and preferences dictionaries.

    """
    config_path = config_path or os.path.join(
        os.path.expanduser("~"), ".config", "bcabrera", "daily_tasks"
    )

    if not os.path.exists(config_path):
        print(f"Creating configuration directory at {config_path}")
        os.makedirs(config_path)
    else:
        print(f"Configuration directory found at {config_path}")

    settings = Settings(**_load_config(config_path, "settings"))
    preferences = Preferences(**_load_config(config_path, "preferences"))

    return settings, preferences

def _load_config(config_path: str, key: str) -> Dict[str, str]:
    current_file_path = os.path.abspath(__file__)
    defaults_path = os.path.join(
        os.path.dirname(current_file_path),
        "../data", f"default_{key}.json"
    )

    with open(defaults_path, "r", encoding="utf-8") as fh:
        print(f"Loading {key} with default values from {defaults_path}")
        values = json.load(fh)

    overwrite_path = os.path.join(config_path, f"{key}.json")
    if os.path.exists(overwrite_path):
        with open(overwrite_path, "r", encoding="utf-8") as fh:
            print(f"Overwriting {key} with values from {overwrite_path}")
            current_values = json.load(fh)
            values.update(current_values)
    else:
        with open(overwrite_path, "w+", encoding="utf-8") as fh:
            print(f"Writing default values to {overwrite_path}")
            if len(values) > 0:
                json.dump(values, fh)
            else:
                fh.write("{}")

    return values
