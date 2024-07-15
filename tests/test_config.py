import os
import unittest
import json
from daily_tasks.config import _load_config


class TestLoadConfig(unittest.TestCase):
    def setUp(self):
        self.config_path = os.path.join(os.path.expanduser("~"), ".config", "bcabrera", "daily_tasks")
        self.key = "settings"
        self.defaults_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data", f"default_{self.key}.json"))
        self.overwrite_path = os.path.join(self.config_path, f"{self.key}.json")

    def tearDown(self):
        if os.path.exists(self.overwrite_path):
            os.remove(self.overwrite_path)

    def test_load_config_with_defaults(self):
        values = _load_config(self.config_path, self.key)
        with open(self.defaults_path, "r", encoding="utf-8") as fh:
            expected_values = json.load(fh)
        self.assertEqual(values, expected_values)


if __name__ == "__main__":
    unittest.main()