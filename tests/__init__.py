import tempfile
from daily_tasks.models import Settings, Preferences, JSONSettings, GTKUIPreferences, SQLiteSettings


test_settings = Settings(
    json_settings=JSONSettings(tasks_path=tempfile.mktemp()),
    sqlite_settings=SQLiteSettings(db_path=tempfile.mktemp())
)

test_preferences = Preferences(
    gtk_ui=GTKUIPreferences(
        default_window_height=600,
        default_window_width=800,
        max_window_height=800,
        max_window_width=1000
    )
)
