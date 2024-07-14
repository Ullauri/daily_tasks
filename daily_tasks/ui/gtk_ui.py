import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from typing import Callable, List, Dict, Any
from daily_tasks.ui import UI
from daily_tasks.models import Task, TaskFilter, Settings, Preferences


class GTKTaskOverview(UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = Gtk.Window(title="Task Manager")
        self.window.set_border_width(10)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(self.dt_preferences.gtk_ui.default_window_width, self.dt_preferences.gtk_ui.default_window_height)

        self.on_filter_tasks_callback = None
        self.on_create_task_callback = None
        self.on_edit_task_callback = None
        self.on_delete_task_callback = None
        self.on_complete_task_callback = None
        self.on_get_task_callback = None
        self.on_get_task_by_index_callback = None
        self.on_get_task_by_id_callback = None

        # Creating the UI
        self.grid = Gtk.Grid()
        self.window.add(self.grid)

        # Task List
        self.task_list_store = Gtk.ListStore(str, str, str)
        self.__update_task_list_store(kwargs["init_tasks"])

        self.task_treeview = Gtk.TreeView(model=self.task_list_store)
        self.task_treeview.set_vexpand(True)

        for i, column_title in enumerate(["Title", "Description", "Completed"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.task_treeview.append_column(column)

        self.grid.attach(self.task_treeview, 0, 0, 6, 1)

        # Filter Buttons
        self.list_active_button = Gtk.Button(label="List Active")
        self.grid.attach(self.list_active_button, 0, 1, 2, 1)

        self.list_completed_button = Gtk.Button(label="List Completed")
        self.grid.attach(self.list_completed_button, 2, 1, 2, 1)

        self.list_all_button = Gtk.Button(label="List All")
        self.grid.attach(self.list_all_button, 4, 1, 2, 1)

        # CRUD Buttons
        self.create_button = Gtk.Button(label="Create Task")
        self.grid.attach(self.create_button, 0, 2, 1, 1)

        self.edit_button = Gtk.Button(label="Edit Task")
        self.grid.attach(self.edit_button, 1, 2, 1, 1)

        self.delete_button = Gtk.Button(label="Delete Task")
        self.grid.attach(self.delete_button, 2, 2, 1, 1)

        self.complete_button = Gtk.Button(label="Complete Task")
        self.grid.attach(self.complete_button, 3, 2, 1, 1)

        self.view_button = Gtk.Button(label="View Task")
        self.grid.attach(self.view_button, 4, 2, 1, 1)

    def __update_task_list_store(self, tasks: List[Task] = None):
        self.task_list_store.clear()
        for task in tasks:
            self.task_list_store.append([task.title, task.description_display_text(), str(task.completed)])

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
        self.on_create_task_callback = on_create_task_callback
        self.on_edit_task_callback = on_edit_task_callback
        self.on_delete_task_callback = on_delete_task_callback
        self.on_complete_task_callback = on_complete_task_callback
        self.on_filter_tasks_callback = on_filter_tasks_callback
        self.on_get_task_by_index_callback = on_get_task_by_index_callback
        self.on_get_task_by_id_callback = on_get_task_by_id_callback

        self.list_active_button.connect("clicked", self.on_list_active)
        self.list_completed_button.connect("clicked", self.on_list_completed)
        self.list_all_button.connect("clicked", self.on_list_all)
        self.create_button.connect("clicked", self.on_create_task)
        self.edit_button.connect("clicked", self.on_edit_task)
        self.delete_button.connect("clicked", self.on_delete_task)
        self.complete_button.connect("clicked", self.on_complete_task)
        self.view_button.connect("clicked", self.on_view_task)

    def on_create_task(self, widget):
        dialog = TaskDialog(self.window, title="Create Task")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            data = dialog.get_task_data()
            tasks = self.on_create_task_callback(Task(**data))
            self.__update_task_list_store(tasks)

        dialog.destroy()

    def on_edit_task(self, widget):
        selection = self.task_treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            task_index = model.get_path(treeiter)[0]
            task = self.on_get_task_by_index_callback(task_index)
            task_id = task.id

            dialog = TaskDialog(self.window, title="Edit Task", task=task, dt_settings=self.dt_settings, dt_preferences=self.dt_preferences)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                data = dialog.get_task_data()
                tasks = self.on_edit_task_callback(task_id, data)
                self.__update_task_list_store(tasks)

            dialog.destroy()

    def on_delete_task(self, widget):
        selection = self.task_treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            task_index = model.get_path(treeiter)[0]
            task = self.on_get_task_by_index_callback(task_index)
            task_id = task.id

            tasks = self.on_delete_task_callback(task_id)
            self.__update_task_list_store(tasks)

    def on_complete_task(self, widget):
        selection = self.task_treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            task_index = model.get_path(treeiter)[0]
            task = self.on_get_task_by_index_callback(task_index)
            task_id = task.id

            tasks = self.on_complete_task_callback(task_id)
            self.__update_task_list_store(tasks)

    def on_view_task(self, widget):
        selection = self.task_treeview.get_selection()
        model, treeiter = selection.get_selected()

        if treeiter is not None:
            task_index = model.get_path(treeiter)[0]
            task = self.on_get_task_by_index_callback(task_index)

            dialog = ViewTaskDialog(self.window, task, dt_settings=self.dt_settings, dt_preferences=self.dt_preferences)
            dialog.run()
            dialog.destroy()

    def on_list_active(self, widget):
        tasks = self.on_filter_tasks_callback(TaskFilter.ACTIVE)
        self.__update_task_list_store(tasks)

    def on_list_completed(self, widget):
        tasks = self.on_filter_tasks_callback(TaskFilter.COMPLETED)
        self.__update_task_list_store(tasks)

    def on_list_all(self, widget):
        tasks = self.on_filter_tasks_callback(TaskFilter.ALL)
        self.__update_task_list_store(tasks)

    def launch(self):
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        Gtk.main()


class TaskDialog(Gtk.Dialog):
    def __init__(self, parent, title, task=None, dt_settings: Settings=None, dt_preferences: Preferences=None):
        super().__init__(title=title, transient_for=parent, flags=0)
        self.dt_settings = dt_settings
        self.dt_preferences = dt_preferences

        self.set_default_size(200, 100)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.task = task

        box = self.get_content_area()
        self.grid = Gtk.Grid()
        box.add(self.grid)

        self.title_entry = Gtk.Entry()
        self.description_entry = Gtk.Entry()

        if task:
            self.title_entry.set_text(task.title)
            self.description_entry.set_text(task.description)

        self.grid.attach(Gtk.Label(label="Title"), 0, 0, 1, 1)
        self.grid.attach(self.title_entry, 1, 0, 1, 1)

        self.grid.attach(Gtk.Label(label="Description"), 0, 1, 1, 1)
        self.grid.attach(self.description_entry, 1, 1, 1, 1)

        self.show_all()

    def get_task_data(self) -> Dict[str, Any]:
        return {
            "title": self.title_entry.get_text(),
            "description": self.description_entry.get_text()
        }


class ViewTaskDialog(Gtk.Dialog):
    def __init__(self, parent, task, dt_settings: Settings=None, dt_preferences: Preferences=None):
        super().__init__(title="View Task", transient_for=parent, flags=0)
        self.dt_settings = dt_settings
        self.dt_preferences = dt_preferences

        self.set_default_size(self.dt_preferences.gtk_ui.max_window_width, self.dt_preferences.gtk_ui.max_window_height)

        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        box = self.get_content_area()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_min_content_width(self.dt_preferences.gtk_ui.max_window_width)
        scrolled_window.set_min_content_height(self.dt_preferences.gtk_ui.max_window_height)
        box.add(scrolled_window)

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        scrolled_window.add_with_viewport(self.grid)

        self.add_label_to_grid("Title", task.title, 0)
        self.add_label_to_grid("Description", task.description, 1)
        self.add_label_to_grid("Completed", str(task.completed), 2)

        self.show_all()

    def add_label_to_grid(self, label_text, value_text, row):
        label = Gtk.Label(label=label_text)
        # Align to the left
        label.set_xalign(0)
        value = Gtk.Label(label=value_text)
         # Align to the left
        value.set_xalign(0)
        # Allow text to wrap
        value.set_line_wrap(True)
        self.grid.attach(label, 0, row, 1, 1)
        self.grid.attach(value, 1, row, 1, 1)
