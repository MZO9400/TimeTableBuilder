import tkinter

from graphics import Graphics
from graphics import AddNewRule
from graphics import Queries
from graphics import TimeTable
from helpers.functions import verify_time

BUTTON_WIDTH = 25
BUTTON_HEIGHT = 10


class TimeTableBuilder(Graphics):
    def __init__(self, course_alloc, window_title="Time Table Builder"):
        super().__init__(window_title=window_title)

        self.course_alloc = course_alloc

        self.sub_window = None
        self.button_show_time_table = None
        self.button_add_new_rule = None
        self.button_queries = None

        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)

    def __init_window__(self):
        self.window.columnconfigure(0)
        self.window.columnconfigure(1)

        self.window.rowconfigure(1)
        self.window.rowconfigure(0)

        self.button_show_time_table = tkinter.Button(
            self.window,
            text="Display Time Table",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.create_time_table)
        self.button_show_time_table.grid(row=1, column=1)

        self.button_add_new_rule = tkinter.Button(
            self.window,
            text="Add new data",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            command=self.create_add_new_rule)
        self.button_add_new_rule.grid(row=1, column=2)

        self.button_queries = tkinter.Button(
            self.window,
            text="Queries",
            width=BUTTON_WIDTH * 2,
            height=BUTTON_HEIGHT,
            command=self.create_queries)
        self.button_queries.grid(row=2, column=1, columnspan=2)

    def on_exit(self):
        self.delete_sub_window()
        self.window.destroy()

    def delete_sub_window(self):
        if self.sub_window is not None:
            self.sub_window.window.destroy()
            self.sub_window = None

    def create_time_table(self):
        self.delete_sub_window()
        self.sub_window = TimeTable(self, self.get_time_table_data)
        self.sub_window.start()

    def create_add_new_rule(self):
        self.delete_sub_window()
        self.sub_window = AddNewRule(self, self.add_new_rule)
        self.sub_window.start()

    def create_queries(self):
        self.delete_sub_window()
        self.sub_window = Queries(self, self.course_alloc)
        self.sub_window.start()

    def get_time_table_data(self, section=None):
        query = self.course_alloc.query
        return query(section=section) if section else query()

    def add_new_rule(self, room, day, section, course, instructor, time):
        if verify_time(room, day, section, course, instructor, time):
            return self.course_alloc.insert(room, day, section, course, instructor, time)
        return False
